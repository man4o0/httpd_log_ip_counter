import re
import ipaddress

log = open('PUT_THE_PATH_OF_YOUR_LOG_HERE')
log_file = ("".join(log))

list_of_ips = []
report_ips = {}


def find_and_match_ips_from_log(log, ips):
    pattern_ip = r"\b(\d{1,3})(.)(\d{1,3})(\.)(\d{1,3})(\.)(\d{1,3})\b"
    matches = re.findall(pattern_ip, log)
    for match in matches:
        first_octet = int(match[0])
        second_octet = int(match[2])
        third_octet = int(match[4])
        forth_octet = int(match[6])
        if len(match) == 7 and (
                254 > second_octet > 0 and 254 > third_octet >= 0 and 254 > forth_octet >= 0 and 254 > first_octet >= 0) and \
                match[1] == '.' and match[3] == '.':
            ips.append("".join(match))


def valid_public_ip_addr(ips, report):
    for ip in ips:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_global:
            if ip not in report_ips:
                report[ip] = 0
            report[ip] += 1


def report_occurence_of_ips(report):
    print(f"Log {log.name}")
    print("-" * 40)

    # Sort the report items by IP addresses (key) in ascending order
    sorted_report = sorted(report.items(), key=lambda x: x[0])
    # Then, sort by count (value) in descending order
    sorted_report = sorted(sorted_report, key=lambda x: x[1], reverse=True)

    for ip, count in sorted_report:
        print(f"Public IP: {ip} - {count} ")




find_and_match_ips_from_log(log_file, list_of_ips)
valid_public_ip_addr(list_of_ips, report_ips)
report_occurence_of_ips(report_ips)
