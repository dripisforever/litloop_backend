// Creating EFS cluster

resource "aws_efs_file_system" "httpd_efs" {
  depends_on = [
    aws_security_group.efs_sg
  ]
  creation_token = "efs"
  tags = {
    Name = "httpdstorage"
  }
}

resource "aws_efs_mount_target" "efs_mount" {
  depends_on = [
    aws_efs_file_system.httpd_efs
  ]
  for_each        = data.aws_subnet_ids.default_subnet.ids
  file_system_id  = aws_efs_file_system.httpd_efs.id
  subnet_id       = each.value
  security_groups = ["${aws_security_group.efs_sg.id}"]
}
