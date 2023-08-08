// Creating S3 bucket.

resource "aws_s3_bucket" "httpds3" {
  bucket = "raktim-httpd-files"
  acl    = "public-read"
}

//Putting Objects in S3 Bucket

resource "aws_s3_bucket_object" "s3_object" {
  bucket = aws_s3_bucket.httpds3.bucket
  key    = "Raktim.JPG"
  source = "C:/Users/rakti/OneDrive/Desktop/Raktim.JPG"
  acl    = "public-read"
}

// Creating Cloud Front Distribution.

locals {
  s3_origin_id = aws_s3_bucket.httpds3.id
}

resource "aws_cloudfront_distribution" "CloudFrontAccess" {

  depends_on = [
    aws_s3_bucket_object.s3_object,
  ]

  origin {
    domain_name = aws_s3_bucket.httpds3.bucket_regional_domain_name
    origin_id   = local.s3_origin_id
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "s3bucket-access"

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.s3_origin_id
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "allow-all"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }
  # Cache behavior with precedence 0
  ordered_cache_behavior {
    path_pattern     = "/content/immutable/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = local.s3_origin_id
    forwarded_values {
      query_string = false
      headers      = ["Origin"]
      cookies {
        forward = "none"
      }
    }
    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }
  # Cache behavior with precedence 1
  ordered_cache_behavior {
    path_pattern     = "/content/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.s3_origin_id
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }
  price_class = "PriceClass_200"
  restrictions {
    geo_restriction {
      restriction_type = "blacklist"
      locations        = ["CA"]
    }
  }
  tags = {
    Environment = "production"
  }
  viewer_certificate {
    cloudfront_default_certificate = true
  }
  retain_on_delete = true
}
