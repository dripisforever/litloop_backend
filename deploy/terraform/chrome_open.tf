// Finally opening the browser to that particular html sites to see how It's working.

resource "null_resource" "ChromeOpen"  {
depends_on = [
    aws_instance.HttpdInstance_2,
  ]

	provisioner "local-exec" {
	    command = "chrome  ${aws_instance.HttpdInstance_1.public_ip}/Raktim.html ${aws_instance.HttpdInstance_2.public_ip}/Raktim.html"
  	}
}
