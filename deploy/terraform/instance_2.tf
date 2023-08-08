// creating the 2nd EC2 Instance

resource "aws_instance" "HttpdInstance_2" {

  depends_on = [
      aws_instance.HttpdInstance_1,
  ]

  ami           = "ami-0e306788ff2473ccb"
  instance_type = "t2.micro"
  key_name      = var.EC2_Key
  security_groups = [ "${aws_security_group.httpd_security.name}" ]

  connection {
    type     = "ssh"
    user     = "ec2-user"
    private_key = tls_private_key.httpdkey.private_key_pem
    host     = aws_instance.HttpdInstance_2.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo yum install httpd -y",
      "sudo systemctl restart httpd",
      "sudo yum install -y amazon-efs-utils",
      "sudo mount -t efs -o tls ${aws_efs_file_system.httpd_efs.id}:/ /var/www/html",
     ]
  }

  tags = {
    Name = "HttpdServer2"
  }
}
