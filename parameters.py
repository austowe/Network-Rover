#add or remove ports
target_ports = [22, 53, 80, 443, 25, 110, 143, 3389, 587, 3306, 1433, 5900, 8000, 8080, 8443, 8888]
#Lower is faster but less accurate, recommended .2
ping_timeout = .2
 #Lower is faster but less accurate, recommended .1
port_timeout = .1
output_to_csv = False
verbose_output = True