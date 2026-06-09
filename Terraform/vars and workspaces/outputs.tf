output "Instance_Public_IP" {
  description = "My Instance Public IP"
  value       = aws_instance.webserver.public_ip
}

output "Instance_Private_IP" {
  description = "My Instance Priavte IP"
  value       = aws_instance.webserver.private_ip
}

output "Instance_id" {
  description = "My Instance id"
  value       = aws_instance.webserver.id
}