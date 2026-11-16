#!/usr/bin/env bash
# Block non-public destination IPs at the kernel egress boundary.
# This covers redirects, DNS aliases/rebinding, and IPv4-mapped IPv6:
# filtering only the original URL does not.
set -euo pipefail

v4=LC_PRIVATE_V4
v6=LC_PRIVATE_V6

install_guard() {
  # A failure to install *either* address family's rules must abort the job.
  sudo -n iptables -w -N "$v4"
  sudo -n ip6tables -w -N "$v6"

  # Let response packets for already-established local sessions return.
  # New outbound connections to private destinations are still denied.
  sudo -n iptables -w -A "$v4" -m conntrack --ctstate ESTABLISHED,RELATED -j RETURN
  sudo -n ip6tables -w -A "$v6" -m conntrack --ctstate ESTABLISHED,RELATED -j RETURN

  # Allow only UDP DNS to a local stub resolver; TCP/53 remains blocked
  # so an HTTP endpoint listening there cannot bypass the egress policy.
  sudo -n iptables -w -A "$v4" -d 127.0.0.0/8 -p udp --dport 53 -j RETURN
  sudo -n ip6tables -w -A "$v6" -d ::1/128 -p udp --dport 53 -j RETURN

  # IANA non-global and private IPv4 ranges (including metadata/link-local,
  # shared, loopback, documentation, benchmarking, multicast and reserved).
  for cidr in \
    0.0.0.0/8 10.0.0.0/8 100.64.0.0/10 127.0.0.0/8 \
    169.254.0.0/16 172.16.0.0/12 192.0.0.0/24 192.0.2.0/24 \
    192.88.99.0/24 192.168.0.0/16 198.18.0.0/15 \
    198.51.100.0/24 203.0.113.0/24 224.0.0.0/4 240.0.0.0/4; do
    sudo -n iptables -w -A "$v4" -d "$cidr" -j REJECT
  done

  # Reject non-global IPv6, translation, and tunnel prefixes that could
  # otherwise encode IPv4 destinations. Ordinary global IPv6 stays usable.
  for cidr in \
    ::/96 ::1/128 ::ffff:0:0/96 64:ff9b::/96 64:ff9b:1::/48 \
    100::/64 2001::/32 2001:2::/48 2001:10::/28 \
    2001:20::/28 2001:db8::/32 2002::/16 \
    fc00::/7 fe80::/10 ff00::/8; do
    sudo -n ip6tables -w -A "$v6" -d "$cidr" -j REJECT
  done

  # Install hooks *after* both address families are fully configured.
  sudo -n iptables -w -I OUTPUT 1 -j "$v4"
  sudo -n ip6tables -w -I OUTPUT 1 -j "$v6"
  echo "Non-public destination egress policy installed for IPv4 and IPv6"
}

remove_guard() {
  # The job runs on a disposable runner; cleanup is best effort, especially
  # if installation failed halfway. Never run Lychee on installation failure.
  sudo -n iptables -w -D OUTPUT -j "$v4" 2>/dev/null || true
  sudo -n ip6tables -w -D OUTPUT -j "$v6" 2>/dev/null || true
  sudo -n iptables -w -F "$v4" 2>/dev/null || true
  sudo -n ip6tables -w -F "$v6" 2>/dev/null || true
  sudo -n iptables -w -X "$v4" 2>/dev/null || true
  sudo -n ip6tables -w -X "$v6" 2>/dev/null || true
  echo "Non-public destination egress policy removed"
}

case "${1:-}" in
  install) install_guard ;;
  remove) remove_guard ;;
  *) echo "Usage: $0 install|remove" >&2; exit 2 ;;
esac
