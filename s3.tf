resource "aws_s3_bucket_public_access_block" "public_bucket" {
  bucket = aws_s3_bucket.public_bucket.id

  # Disable all “block public access” settings:
  block_public_acls       = false
  block_public_policy     = false   # explicitly allow public bucket policies
  ignore_public_acls      = false
  restrict_public_buckets = false
}
