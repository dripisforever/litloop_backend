// creating the 1st EC2 Instance

resource "aws_instance" "HttpdInstance_1" {

  depends_on = [
    aws_efs_file_system.httpd_efs,
    aws_efs_mount_target.efs_mount,
    aws_cloudfront_distribution.CloudFrontAccess,
  ]

  ami           = "ami-0e306788ff2473ccb"
  instance_type = "t2.micro"
  key_name      = var.EC2_Key
  security_groups = [ "${aws_security_group.httpd_security.name}" ]

  connection {
    type     = "ssh"
    user     = "ec2-user"
    private_key = tls_private_key.httpdkey.private_key_pem
    host     = aws_instance.HttpdInstance_1.public_ip
  }
  
  provisioner "remote-exec" {
    inline = [
      "sudo yum install httpd git -y",
      "sudo systemctl restart httpd",
      "sudo yum install -y amazon-efs-utils",
      "sudo mount -t efs -o tls ${aws_efs_file_system.httpd_efs.id}:/ /var/www/html",
      "sudo git clone https://github.com/raktim00/DevOpsHW.git /var/www/html",
      "echo '<img src='https://${aws_cloudfront_distribution.CloudFrontAccess.domain_name}/Raktim.JPG' width='300' height='330'>' | sudo tee -a /var/www/html/Raktim.html",
    ]
  }

  tags = {
    Name = "HttpdServer1"
  }
}
