
class Publisher(TimeStampedModel, IndestructibleModel):

    """
    A publisher that displays advertising from the ad server.

    A publisher represents a site or collection of sites that displays advertising.
    Advertisers can opt-in to displaying ads on different publishers.

    An example of a publisher would be Read the Docs, our first publisher.
    """

    name = models.CharField(_("Name"), max_length=200)
    slug = models.SlugField(_("Publisher Slug"), max_length=200, unique=True)

    revenue_share_percentage = models.FloatField(
        default=70.0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Percentage of advertising revenue shared with this publisher"),
    )

    default_keywords = models.CharField(
        _("Default keywords"),
        max_length=250,
        help_text=_("A CSV of default keywords for this property. Used for targeting."),
        default="",
        blank=True,
    )

    unauthed_ad_decisions = models.BooleanField(
        default=True,
        help_text=_(
            "Whether this publisher allows unauthenticated ad decision API requests (eg. JSONP)"
        ),
    )
    disabled = models.BooleanField(
        default=False,
        help_text=_("Completely disable this publisher"),
    )

    saas = models.BooleanField(
        default=False,
        help_text=_(
            "This published is configured as a SaaS customer. They will be billed by usage instead of paid out."
        ),
    )

    # Default to False so that we can use this as an "approved" flag for publishers
    allow_paid_campaigns = models.BooleanField(_("Allow paid campaigns"), default=False)
    allow_affiliate_campaigns = models.BooleanField(
        _("Allow affiliate campaigns"), default=False
    )
    allow_community_campaigns = models.BooleanField(
        _("Allow community campaigns"),
        default=True,
        help_text="These are unpaid campaigns that support non-profit projects in our community. Shown only when no paid ads are available",
    )
    allow_house_campaigns = models.BooleanField(
        _("Allow house campaigns"),
        default=True,
        help_text="These are ads for EthicalAds itself. Shown only when no paid ads are available.",
    )

    # Payout information
    skip_payouts = models.BooleanField(
        _("Skip payouts"),
        default=False,
        help_text=_(
            "Enable this to temporarily disable payouts. They will be processed again once you uncheck this."
        ),
    )
    payout_method = models.CharField(
        max_length=100,
        choices=PUBLISHER_PAYOUT_METHODS,
        blank=True,
        null=True,
        default=None,
    )
    djstripe_account = models.ForeignKey(
        djstripe_models.Account,
        verbose_name=_("Stripe connected account"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )

    # Deprecated - migrate to `stripe_account`
    stripe_connected_account_id = models.CharField(
        _("Stripe connected account ID"),
        max_length=200,
        blank=True,
        null=True,
        default=None,
    )
    open_collective_name = models.CharField(
        _("Open Collective name"), max_length=200, blank=True, null=True, default=None
    )
    paypal_email = models.EmailField(
        _("PayPal email address"), blank=True, null=True, default=None
    )

    # This overrides settings.ADSERVER_RECORD_VIEWS for a specific publisher
    # Details of each ad view are written to the database.
    # Setting this can result in some performance degradation and a bloated database,
    # but note that all Offers are stored by default.
    record_views = models.BooleanField(
        default=False,
        help_text=_("Record each ad view from this publisher to the database"),
    )
    record_placements = models.BooleanField(
        default=False, help_text=_("Record placement impressions for this publisher")
    )
    # This defaults to False, so publishers have to ask for it.
    render_pixel = models.BooleanField(
        default=False,
        help_text=_(
            "Render ethical-pixel in ad templates. This is needed for users not using the ad client."
        ),
    )
    cache_ads = models.BooleanField(
        default=True,
        help_text=_(
            "Cache this publishers ad requests. Disable for special cases (eg. SaaS users)"
        ),
    )

    # Denormalized fields
    sampled_ctr = models.FloatField(
        default=0.0,
        help_text=_(
            "A periodically calculated CTR from a sample of ads on this publisher."
        ),
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ("name",)

        permissions = [
            ("staff_publisher_fields", "Can view staff publisher fields in reports"),
        ]

    def __str__(self):
        """Simple override."""
        return self.name

    def get_absolute_url(self):
        return reverse("publisher_report", kwargs={"publisher_slug": self.slug})

    @property
    def keywords(self):
        """
        Parses database keywords and ensures consistency.

        - Lowercases all tags
        - Converts underscores to hyphens
        - Slugifies tags
        - Removes empty tags

        Similar logic to RTD ``readthedocs.projects.tag_utils.rtd_parse_tags``.
        """
        if self.default_keywords:
            return_keywords = []
            keyword_list = self.default_keywords.split(",")
            for keyword in keyword_list:
                keyword = keyword.lower().replace("_", "-")
                keyword = slugify(keyword)
                if keyword:
                    return_keywords.append(keyword)
            return return_keywords
        return []

    def total_payout_sum(self):
        """The total amount ever paid out to this publisher."""
        total = self.payouts.filter(status=PAID).aggregate(
            total=models.Sum("amount", output_field=models.DecimalField())
        )["total"]
        if total:
            return total
        return 0

    def payout_url(self):
        if self.payout_method == PAYOUT_STRIPE and self.djstripe_account.id:
            return f"https://dashboard.stripe.com/connect/accounts/{self.djstripe_account.id}"
        if self.payout_method == PAYOUT_OPENCOLLECTIVE and self.open_collective_name:
            return f"https://opencollective.com/{self.open_collective_name}"
        if self.payout_method == PAYOUT_PAYPAL and self.paypal_email:
            return "https://www.paypal.com/myaccount/transfer/homepage/pay"
        return ""


class PublisherGroup(TimeStampedModel):

    """Group of publishers that can be targeted by advertiser's campaigns."""

    name = models.CharField(
        _("Name"), max_length=200, help_text=_("Visible to advertisers")
    )
    slug = models.SlugField(_("Publisher group slug"), max_length=200, unique=True)

    publishers = models.ManyToManyField(
        Publisher,
        related_name="publisher_groups",
        blank=True,
        help_text=_("A group of publishers that can be targeted by advertisers"),
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        """Simple override."""
        return self.name
