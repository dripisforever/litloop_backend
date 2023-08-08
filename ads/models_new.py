class IndestructibleQuerySet(models.QuerySet):

    """A queryset object without the delete option."""

    def delete(self):
        """Always raises ``IntegrityError``."""
        raise IntegrityError


class IndestructibleManager(models.Manager):

    """A model manager that generates ``IndestructibleQuerySets``."""

    def get_queryset(self):
        return IndestructibleQuerySet(self.model, using=self._db)


class IndestructibleModel(models.Model):

    """A model that disallows the delete method or deleting at the queryset level."""

    objects = IndestructibleManager()

    def delete(self, using=None, keep_parents=False):
        """Always raises ``IntegrityError``."""
        raise IntegrityError

    class Meta:
        abstract = True


class AdBase(TimeStampedModel, IndestructibleModel):

    """A base class for data on ad views and clicks."""

    DIV_MAXLENGTH = 100

    date = models.DateTimeField(_("Impression date"), db_index=True)

    publisher = models.ForeignKey(
        Publisher, null=True, blank=True, on_delete=models.PROTECT
    )

    # This field is overridden in subclasses
    advertisement = models.ForeignKey(
        Advertisement,
        max_length=255,
        related_name="clicks_or_views",
        on_delete=models.PROTECT,
    )

    # User Data
    ip = models.GenericIPAddressField(_("Ip Address"))  # anonymized
    user_agent = models.CharField(
        _("User Agent"), max_length=1000, blank=True, null=True
    )
    # Client IDs are used primarily for fraud and short term (sub-day) frequency capping
    client_id = models.CharField(_("Client ID"), max_length=1000, blank=True, null=True)
    country = CountryField(null=True)
    url = models.CharField(_("Page URL"), max_length=10000, blank=True, null=True)

    # Fields derived from the user agent - these should not be user identifiable
    browser_family = models.CharField(
        _("Browser Family"), max_length=1000, blank=True, null=True, default=None
    )
    os_family = models.CharField(
        _("Operating System Family"),
        max_length=1000,
        blank=True,
        null=True,
        default=None,
    )

    # Client data
    keywords = JSONField(_("Keyword targeting for this view"), blank=True, null=True)
    div_id = models.CharField(
        _("Div id"), blank=True, null=True, max_length=DIV_MAXLENGTH
    )
    # This locked up the DB for a long time trying to write to our huge View table,
    # so we made it a Text field instead of a FK.
    ad_type_slug = models.CharField(_("Ad type"), blank=True, null=True, max_length=100)

    is_bot = models.BooleanField(default=False)
    is_mobile = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)

    impression_type = None

    class Meta:
        abstract = True

    def __str__(self):
        """Simple override."""
        return "%s on %s (%s)" % (self._meta.object_name, self.advertisement, self.url)

    def get_absolute_url(self):
        return self.url


class Click(AdBase):

    """Contains data on ad clicks."""

    advertisement = models.ForeignKey(
        Advertisement, max_length=255, related_name="clicks", on_delete=models.PROTECT
    )
    impression_type = CLICKS


class View(AdBase):

    """Contains data on ad views."""

    advertisement = models.ForeignKey(
        Advertisement, max_length=255, related_name="views", on_delete=models.PROTECT
    )
    impression_type = VIEWS


class BaseImpression(TimeStampedModel, models.Model):

    """Statistics for tracking."""

    date = models.DateField(_("Date"), db_index=True)

    # Decisions are a superset of all Offers.
    # Every API request that comes in results in a Decision,
    # and an Offer is only created when we actually offer an ad.
    decisions = models.PositiveIntegerField(
        _("Decisions"),
        default=0,
        help_text=_(
            "The number of times the Ad Decision API was called. "
            "The server might not respond with an ad if there isn't inventory."
        ),
    )

    # Offers include cases where the server returned an ad
    # but the client didn't load it
    # or the client didn't qualify as a view (staff, blocklisted, etc.)
    offers = models.PositiveIntegerField(
        _("Offers"),
        default=0,
        help_text=_(
            "The number of times an ad was proposed by the ad server. "
            "The client may not load the ad (a view) for a variety of reasons "
        ),
    )

    # Views & Clicks don't count actions that are blocklisted, done by staff, bots, etc.
    views = models.PositiveIntegerField(
        _("Views"),
        default=0,
        help_text=_("Number of times the ad was legitimately viewed"),
    )
    clicks = models.PositiveIntegerField(
        _("Clicks"),
        default=0,
        help_text=_("Number of times the ad was legitimately clicked"),
    )

    class Meta:
        abstract = True

    @property
    def view_ratio(self):
        if self.offers == 0:
            return 0  # Don't divide by 0
        return float(float(self.views) / float(self.offers) * 100)

    @property
    def click_ratio(self):
        if self.views == 0:
            return 0  # Don't divide by 0
        return "%.3f" % float(float(self.clicks) / float(self.views) * 100)


class AdImpression(BaseImpression):

    """
    Track stats around how successful this ad has been.

    Indexed one per ad per day per publisher.
    """

    publisher = models.ForeignKey(
        Publisher, null=True, blank=True, on_delete=models.PROTECT
    )
    advertisement = models.ForeignKey(
        Advertisement, related_name="impressions", on_delete=models.PROTECT, null=True
    )
    view_time = models.PositiveIntegerField(
        _("Seconds that the ad was in view"),
        null=True,
    )

    class Meta:
        # We must also constrain when the `advertisement` is null
        constraints = (
            UniqueConstraint(
                fields=("publisher", "date"),
                condition=models.Q(advertisement=None),
                name="null_offer_unique",
            ),
        )
        ordering = ("-date",)
        unique_together = ("publisher", "advertisement", "date")
        verbose_name_plural = _("Ad impressions")

    def __str__(self):
        """Simple override."""
        return "%s on %s" % (self.advertisement, self.date)
