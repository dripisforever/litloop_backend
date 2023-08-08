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

    # equivalent to user
    publisher = models.ForeignKey(
        Publisher, null=True, blank=True, on_delete=models.PROTECT
    )

    # equivalent to post
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


class PlacementImpression(BaseImpression):

    """
    Create an index of placements for ads.

    Indexed one per ad/publisher/placement per day.
    """

    div_id = models.CharField(max_length=255, null=True, blank=True)
    ad_type_slug = models.CharField(_("Ad type"), blank=True, null=True, max_length=100)
    publisher = models.ForeignKey(
        Publisher, related_name="placement_impressions", on_delete=models.PROTECT
    )
    advertisement = models.ForeignKey(
        Advertisement,
        related_name="placement_impressions",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        ordering = ("-date",)
        unique_together = (
            "publisher",
            "advertisement",
            "date",
            "div_id",
            "ad_type_slug",
        )
        verbose_name_plural = _("Placement impressions")

    def __str__(self):
        """Simple override."""
        return "Placement %s of %s on %s" % (self.div_id, self.advertisement, self.date)


class GeoImpression(BaseImpression):

    """
    Create an index of geo targeting for ads.

    Indexed one per ad/publisher/geo per day.
    """

    country = CountryField()
    publisher = models.ForeignKey(
        Publisher, related_name="geo_impressions", on_delete=models.PROTECT
    )
    advertisement = models.ForeignKey(
        Advertisement,
        related_name="geo_impressions",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        ordering = ("-date",)
        unique_together = ("publisher", "advertisement", "date", "country")

    def __str__(self):
        """Simple override."""
        return "Geo %s of %s on %s" % (self.country, self.advertisement, self.date)


class RegionImpression(BaseImpression):

    """
    Create an index of region geo targeting for ads.

    Indexed one per ad/publisher/region per day.
    """

    region = models.CharField(_("Region"), max_length=100)
    publisher = models.ForeignKey(
        Publisher, related_name="region_impressions", on_delete=models.PROTECT
    )
    advertisement = models.ForeignKey(
        Advertisement,
        related_name="region_impressions",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        ordering = ("-date",)
        unique_together = ("publisher", "advertisement", "date", "region")

    def __str__(self):
        """Simple override."""
        return "Region %s of %s for %s on %s" % (
            self.region,
            self.advertisement,
            self.publisher,
            self.date,
        )


class KeywordImpression(BaseImpression):

    """
    Create an index of keyword targeting for ads.

    Indexed one per ad/publisher/keyword per day.
    """

    keyword = models.CharField(_("Keyword"), max_length=1000)
    publisher = models.ForeignKey(
        Publisher, related_name="keyword_impressions", on_delete=models.PROTECT
    )
    advertisement = models.ForeignKey(
        Advertisement,
        related_name="keyword_impressions",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        ordering = ("-date",)
        unique_together = ("publisher", "advertisement", "date", "keyword")

    def __str__(self):
        """Simple override."""
        return "Keyword %s of %s on %s" % (self.keyword, self.advertisement, self.date)


class UpliftImpression(BaseImpression):

    """
    Create an index of uplift for ads.

    Indexed one per ad/publisher per day.
    This is a subset of AdImpressions created by uplift from the Acceptable Ads program.
    """

    publisher = models.ForeignKey(
        Publisher, related_name="uplift_impressions", on_delete=models.PROTECT
    )
    advertisement = models.ForeignKey(
        Advertisement,
        related_name="uplift_impressions",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        ordering = ("-date",)
        unique_together = ("publisher", "advertisement", "date")

    def __str__(self):
        """Simple override."""
        return "Uplift of %s on %s" % (self.advertisement, self.date)


class RegionTopicImpression(BaseImpression):

    """
    Create an index combining aggregated keywords & geos.

    Indexed one per region/topic/ad/publisher per day.
    """

    region = models.CharField(_("Region"), max_length=100)
    topic = models.CharField(_("Topic"), max_length=100)
    advertisement = models.ForeignKey(
        Advertisement,
        related_name="regiontopic_impressions",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        ordering = ("-date",)
        unique_together = ("date", "region", "topic", "advertisement")

    def __str__(self):
        """Simple override."""
        return f"RegionTopic Impression ({self.region}:{self.topic}) on {self.date}"
