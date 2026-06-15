output "stream_name" {
  description = "Name of the Kinesis price event stream."
  value       = aws_kinesis_stream.price_events.name
}

output "stream_arn" {
  description = "ARN of the Kinesis price event stream."
  value       = aws_kinesis_stream.price_events.arn
}
