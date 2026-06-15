output "function_name" {
  description = "Name of the latest price ingestion Lambda function."
  value       = aws_lambda_function.latest_price_ingestion.function_name
}

output "function_arn" {
  description = "ARN of the latest price ingestion Lambda function."
  value       = aws_lambda_function.latest_price_ingestion.arn
}
