resource "aws_kinesis_stream" "price_events" {
  name             = "${var.project}-${var.environment}-price-events"
  shard_count      = var.shard_count
  retention_period = var.retention_period_hours

  stream_mode_details {
    stream_mode = "PROVISIONED"
  }

  tags = {
    Name        = "${var.project}-${var.environment}-price-events"
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
