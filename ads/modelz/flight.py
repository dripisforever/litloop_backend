
class Flight(TimeStampedModel, IndestructibleModel):

    """
    A flight is a collection of :py:class:`~Advertisement` objects.

    Effectively a flight is a single "ad buy". So if an advertiser wants to
    buy $2000 worth of ads at $2 CPC and run 5 variations, they would have 5
    :py:class:`~Advertisement` objects in a single :py:class:`~Flight`.
    Flights are associated with a :py:class:`~Campaign` and so they have a
    single advertiser.

    At this level, we control:

    * Sold clicks (maximum clicks across all ads in this flight)
    * CPC/CPM which could be 0
    * Targeting parameters (programming language, geo, etc)
    * Start and end date (the end date is a soft target)
    * Whether the flight is live or not

    Since flights contain important historical data around tracking how we bill
    and report to customers, they cannot be deleted once created.
    """

    HIGHEST_PRIORITY_MULTIPLIER = 1000000
    LOWEST_PRIORITY_MULTIPLIER = 1

    name = models.CharField(_("Name"), max_length=200)
    slug = models.SlugField(_("Flight Slug"), max_length=200, unique=True)
    start_date = models.DateField(
        _("Start Date"),
        default=datetime.date.today,
        db_index=True,
        help_text=_("This ad will not be shown before this date"),
    )
    end_date = models.DateField(
        _("End Date"),
        default=default_flight_end_date,
        help_text=_("The target end date for the ad (it may go after this date)"),
    )
    live = models.BooleanField(_("Live"), default=False)
    priority_multiplier = models.IntegerField(
        _("Priority Multiplier"),
        default=LOWEST_PRIORITY_MULTIPLIER,
        validators=[
            MinValueValidator(LOWEST_PRIORITY_MULTIPLIER),
            MaxValueValidator(HIGHEST_PRIORITY_MULTIPLIER),
        ],
        help_text="Multiplies chance of showing this flight's ads [{},{}]".format(
            LOWEST_PRIORITY_MULTIPLIER, HIGHEST_PRIORITY_MULTIPLIER
        ),
    )

    # CPC
    cpc = models.DecimalField(
        _("Cost Per Click"), max_digits=5, decimal_places=2, default=0
    )
    sold_clicks = models.PositiveIntegerField(_("Sold Clicks"), default=0)

    # CPM
    cpm = models.DecimalField(
        _("Cost Per 1k Impressions"), max_digits=5, decimal_places=2, default=0
    )
    sold_impressions = models.PositiveIntegerField(_("Sold Impressions"), default=0)

    campaign = models.ForeignKey(
        Campaign, related_name="flights", on_delete=models.PROTECT
    )

    targeting_parameters = JSONField(
        _("Targeting parameters"),
        blank=True,
        null=True,
        validators=[TargetingParametersValidator()],
    )

    # Denormalized fields
    total_views = models.PositiveIntegerField(
        default=0, help_text=_("Views across all ads in this flight")
    )
    total_clicks = models.PositiveIntegerField(
        default=0, help_text=_("Clicks across all ads in this flight")
    )

    # Connect to Stripe invoice data
    # There can be multiple invoices for a flight
    # (say a 3 month flight billed monthly)
    # and an invoice can cover multiple flights
    invoices = models.ManyToManyField(
        djstripe_models.Invoice,
        verbose_name=_("Stripe invoices"),
        blank=True,
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        """Simple override."""
        return self.name

    @property
    def included_countries(self):
        if not self.targeting_parameters:
            return []
        return self.targeting_parameters.get("include_countries", [])

    @property
    def included_state_provinces(self):
        if not self.targeting_parameters:
            return []
        return self.targeting_parameters.get("include_state_provinces", [])

    @property
    def included_metro_codes(self):
        if not self.targeting_parameters:
            return []
        return self.targeting_parameters.get("include_metro_codes", [])

    @property
    def excluded_countries(self):
        if not self.targeting_parameters:
            return []
        return self.targeting_parameters.get("exclude_countries", [])

    @property
    def included_keywords(self):
        if not self.targeting_parameters:
            return []
        return self.targeting_parameters.get("include_keywords", [])

    @property
    def excluded_keywords(self):
        if not self.targeting_parameters:
            return []
        return self.targeting_parameters.get("exclude_keywords", [])

    @property
    def state(self):
        today = get_ad_day().date()
        if self.live and self.start_date <= today:
            return FLIGHT_STATE_CURRENT
        if self.end_date > today:
            return FLIGHT_STATE_UPCOMING
        return FLIGHT_STATE_PAST

    def get_absolute_url(self):
        return reverse(
            "flight_detail",
            kwargs={
                "advertiser_slug": self.campaign.advertiser.slug,
                "flight_slug": self.slug,
            },
        )

    def get_include_countries_display(self):
        included_country_codes = self.included_countries
        return [COUNTRY_DICT.get(cc, "Unknown") for cc in included_country_codes]

    def get_exclude_countries_display(self):
        excluded_country_codes = self.excluded_countries
        return [COUNTRY_DICT.get(cc, "Unknown") for cc in excluded_country_codes]

    def show_to_geo(self, geo_data):
        """
        Check if a flight is valid for a given country code.

        A ``country_code`` of ``None`` (meaning the user's country is unknown)
        will not match a flight with any ``include_countries`` but wont be
        excluded from any ``exclude_countries``
        """
        if self.included_countries and geo_data.country not in self.included_countries:
            return False
        if (
            self.included_state_provinces
            and geo_data.region not in self.included_state_provinces
        ):
            return False
        if (
            self.included_metro_codes
            and geo_data.metro not in self.included_metro_codes
        ):
            return False
        if self.excluded_countries and geo_data.country in self.excluded_countries:
            return False

        return True

    def show_to_keywords(self, keywords):
        """
        Check if a flight is valid for a given keywords.

        If *any* keywords match the included list, it should be shown.
        If *any* keywords are in the excluded list, it should not be shown.
        """
        keyword_set = set(keywords)
        if self.included_keywords:
            # If no keywords from the page in the include list, don't show this flight
            if not keyword_set.intersection(self.included_keywords):
                return False

        if self.excluded_keywords:
            # If any keyworks from the page in the exclude list, don't show this flight
            if keyword_set.intersection(self.excluded_keywords):
                return False

        return True

    def show_to_mobile(self, is_mobile):
        """Check if a flight is valid for this traffic based on mobile/non-mobile."""
        if not self.targeting_parameters:
            return True

        mobile_traffic_targeting = self.targeting_parameters.get("mobile_traffic")
        if mobile_traffic_targeting == "exclude" and is_mobile:
            return False
        if mobile_traffic_targeting == "only" and not is_mobile:
            return False

        return True

    def sold_days(self):
        # Add one to count both the start and end day
        return max(0, (self.end_date - self.start_date).days) + 1

    def days_remaining(self):
        """Number of days left in a flight."""
        return max(0, (self.end_date - get_ad_day().date()).days)

    def views_today(self):
        # Check for a cached value that would come from an annotated queryset
        if hasattr(self, "flight_views_today"):
            return self.flight_views_today or 0

        aggregation = AdImpression.objects.filter(
            advertisement__in=self.advertisements.all(), date=get_ad_day().date()
        ).aggregate(total_views=models.Sum("views"))["total_views"]

        # The aggregation can be `None` if there are no impressions
        return aggregation or 0

    def clicks_today(self):
        # Check for a cached value that would come from an annotated queryset
        if hasattr(self, "flight_clicks_today"):
            return self.flight_clicks_today or 0

        aggregation = AdImpression.objects.filter(
            advertisement__in=self.advertisements.all(), date=get_ad_day().date()
        ).aggregate(total_clicks=models.Sum("clicks"))["total_clicks"]

        # The aggregation can be `None` if there are no impressions
        return aggregation or 0

    def views_needed_today(self):
        if (
            not self.live
            or self.views_remaining() <= 0
            or self.start_date > get_ad_day().date()
        ):
            return 0

        if self.days_remaining() > 0:
            flight_remaining_percentage = self.days_remaining() / self.sold_days()

            # This is how many views should be remaining this far in the flight
            flight_views_pace = int(self.sold_impressions * flight_remaining_percentage)

            return max(0, self.views_remaining() - flight_views_pace)

        return self.views_remaining()

    def clicks_needed_today(self):
        """Calculates clicks needed based on the impressions this flight's ads have."""
        if (
            not self.live
            or self.clicks_remaining() <= 0
            or self.start_date > get_ad_day().date()
        ):
            return 0

        if self.days_remaining() > 0:
            flight_remaining_percentage = self.days_remaining() / self.sold_days()

            # This is how many clicks we should have remaining this far in the flight
            flight_clicks_pace = int(self.sold_clicks * flight_remaining_percentage)

            return max(0, self.clicks_remaining() - flight_clicks_pace)

        return self.clicks_remaining()

    def weighted_clicks_needed_today(self, publisher=None):
        """
        Calculates clicks needed taking into account a flight's priority.

        For the purpose of clicks needed, 1000 impressions = 1 click (for CPM ads)
        Takes into account value of the flight,
        which causes higher paid and better CTR ads to be prioritized.
        Uses the passed publisher for a better CTR estimate if passed.
        """
        impressions_needed = 0

        # This is naive but we are counting a click as being worth 1,000 views
        impressions_needed += math.ceil(self.views_needed_today() / 1000.0)
        impressions_needed += self.clicks_needed_today()

        if self.cpc:
            # Use the publisher CTR if available
            # Otherwise, use this flight's average CTR
            estimated_ctr = float(self.ctr())
            if publisher and publisher.sampled_ctr > 0.01:
                estimated_ctr = publisher.sampled_ctr

            # Note: CTR is in percent (eg. 0.1 means 0.1% not 0.001)
            estimated_ecpm = float(self.cpc) * estimated_ctr * 10
        else:
            # CPM ads
            estimated_ecpm = float(self.cpm)

        # This prioritizes an ad with estimated eCPM=$1 at the normal rate
        # An ad with estimated eCPM=$2 at 2x the normal rate, eCPM=$3 => 3x normal
        price_priority_value = estimated_ecpm

        # Keep values between 1-10 so we don't penalize the value for lower performance
        # but add value for higher performance without overweighting
        price_priority_value = max(float(price_priority_value), 1.0)
        price_priority_value = min(price_priority_value, 10.0)

        return int(impressions_needed * self.priority_multiplier * price_priority_value)

    def clicks_remaining(self):
        return max(0, self.sold_clicks - self.total_clicks)

    def views_remaining(self):
        return max(0, self.sold_impressions - self.total_views)

    def value_remaining(self):
        """Value ($) remaining on this ad flight."""
        value_clicks_remaining = float(self.clicks_remaining() * self.cpc)
        value_views_remaining = float(self.views_remaining() * self.cpm) / 1000.0
        return value_clicks_remaining + value_views_remaining

    def projected_total_value(self):
        """Total value ($) assuming all sold impressions and clicks are delivered."""
        projected_value_clicks = float(self.sold_clicks * self.cpc)
        projected_value_views = float(self.sold_impressions * self.cpm) / 1000.0
        return projected_value_clicks + projected_value_views

    def total_value(self):
        """Total value ($) so far based on what's been delivered."""
        value_clicks = float(self.total_clicks * self.cpc)
        value_views = float(self.total_views * self.cpm) / 1000.0
        return value_clicks + value_views

    def percent_complete(self):
        projected_total = self.projected_total_value()
        if projected_total > 0:
            return self.total_value() / projected_total * 100
        return 0

    def ctr(self):
        clicks = self.total_clicks
        views = self.total_views
        return calculate_ctr(clicks, views)

    @cached_property
    def active_invoices(self):
        """Get invoices excluding drafts, void, and uncollectable ones."""
        return self.invoices.filter(status__in=(InvoiceStatus.open, InvoiceStatus.paid))
