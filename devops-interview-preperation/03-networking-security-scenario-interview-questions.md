# 🌐 Networking, Firewalls & Cloud Security - 50 Scenario-Based Interview Questions

## Scenario 1: EC2 Instance in Private Subnet Cannot Access Internet via NAT Gateway
**Q:** An EC2 instance inside a Private Subnet (`10.0.2.0/24`) cannot pull software updates from the internet. You created a NAT Gateway in a Public Subnet (`10.0.1.0/24`), but traffic still times out. What routing table misconfiguration caused this?
**A:**
1. Check the **Private Subnet Route Table**: It must contain a route mapping `0.0.0.0/0` -> `nat-gateway-id`.
2. Check the **Public Subnet Route Table** (where the NAT Gateway resides): It must contain a route mapping `0.0.0.0/0` -> `igw-id` (Internet Gateway).
3. Verify NAT Gateway Elastic IP (EIP) attachment and Security Group outbound rules on the instance.

## Scenario 2: Resolving Subnet IP Address Exhaustion (`/28` Subnet)
**Q:** You deployed an Elastic Container Service (ECS) cluster in a `/28` subnet (16 IPs). AWS reserved 5 IPs, leaving only 11 usable. Now container tasks fail to launch due to insufficient IP space. How do you fix this without breaking existing servers?
**A:** You cannot resize an existing subnet CIDR block in AWS.
1. Create a new larger secondary subnet (e.g. `/24` = 251 usable IPs) within the VPC.
2. Associate the new subnet with your ECS Cluster service launch configuration.
3. Migrate tasks to the new subnet and decommission the exhausted `/28` subnet.

## Scenario 3: UFW Firewall Lockout Prevention
**Q:** A junior engineer ran `sudo ufw enable` on a remote Ubuntu server via SSH without adding port rules first, locking everyone out. How do you prevent this scenario in automated Ansible/Terraform provisioning?
**A:** Always explicitly allow the SSH port (`22`) before activating UFW:
```bash
sudo ufw allow 22/tcp comment 'Allow SSH'
sudo ufw --force enable
```
In cloud instances, utilize AWS Security Groups as the primary layer of defense before enabling OS-level firewalls.

## Scenario 4: HTTPS Certificate Trust Warnings (SSL vs TLS)
**Q:** Users accessing your site see `NET::ERR_CERT_COMMON_NAME_INVALID`. You inspect the certificate and notice it was issued for `app.example.com`, but users access `www.example.com`. How do you resolve this?
**A:** The Subject Alternative Name (SAN) of the TLS/SSL certificate does not include the requested domain.
1. Re-issue the TLS certificate via AWS Certificate Manager (ACM) or Let's Encrypt specifying both Subject Names: `example.com` and `*.example.com` (Wildcard).
2. Attach the updated certificate to your Application Load Balancers (ALB) or CloudFront distribution.

## Scenario 5: DNS Resolution Latency & Caching Triage
**Q:** Microservice A calls `api.internal.company.com` 1,000 times per second. Intermittent 5-second latency spikes occur. `tcpdump` reveals thousands of redundant DNS queries to the upstream resolver. How do you optimize this?
**A:** The application does not cache DNS lookups locally and queries the DNS server on every HTTP connection.
1. Enable local DNS caching daemon such as `nscd` or `systemd-resolved` on the host: `sudo systemctl enable --now nscd`.
2. Configure HTTP client connection pooling / Keep-Alive headers in microservice application code to reuse established TCP connections.

## Scenario 6: Troubleshooting Packet Drops via TCP 3-Way Handshake
**Q:** A client tries to connect to web server port `443`. Wireshark shows the client sending `SYN` packets, but receives no `SYN-ACK` response. What are the potential network failure points?
**A:**
1. **Security Group / Firewall:** Incoming TCP 443 traffic is blocked by AWS Security Group or OS firewall (`ufw` / `iptables`).
2. **Server Listening Status:** No process is listening on port 443 (`netstat -tlpn | grep 443`).
3. **Routing / NACL:** Network ACL is blocking inbound TCP 443 or outbound return ephemeral ports (1024-65535).

## Scenario 7: Public vs Private IP NAT Translation
**Q:** Explain how a database server in a private VPC subnet (`10.0.2.15`) downloads a security patch from `archive.ubuntu.com` using NAT Gateway.
**A:**
1. Private EC2 (`10.0.2.15`) sends outbound packet targeting `archive.ubuntu.com:80`.
2. Private subnet route table routes `0.0.0.0/0` to the NAT Gateway in the public subnet.
3. NAT Gateway rewrites the source IP header from private IP `10.0.2.15` to its Public Elastic IP (`54.213.10.15`) and records the mapping in its state table.
4. Response from internet arrives at `54.213.10.15`; NAT Gateway rewrites destination back to `10.0.2.15` and forwards it down to the private instance.

## Scenario 8: CDN Invalidation After Frontend Deployment
**Q:** You deployed new JavaScript bundles to AWS S3 hosted behind AWS CloudFront CDN. Users still see old cached UI components. What command flushes the CDN cache?
**A:** Run an AWS CloudFront Cache Invalidation:
```bash
aws cloudfront create-invalidation --distribution-id E123456789ABC --paths "/*"
```
Best practice: Use cache-busting file hashes (`main.a8f9c1.js`) in build pipelines so HTML updates automatically fetch new bundle names without requiring manual CDN invalidations.

## Scenario 9: Ingress vs Egress Rule Optimization
**Q:** Configure a secure Security Group policy for an application server that only needs to receive HTTPS web traffic from an ALB Security Group (`sg-alb123`) and make outbound calls to an RDS Database Security Group (`sg-rds456`).
**A:**
- **Ingress Rule:** Type: HTTPS (443), Protocol: TCP, Source: Custom (`sg-alb123`).
- **Egress Rule:** Type: MySQL/Aurora (3306), Protocol: TCP, Destination: Custom (`sg-rds456`). Remove default `0.0.0.0/0` egress rule for maximum lockdown.

## Scenario 10: Mitigating DDoS Attacks at Edge
**Q:** Your public web application is experiencing a Layer 7 HTTP flood attack (100,000 requests/sec targeting `/login`). How do you mitigate this using cloud-native tools?
**A:**
1. Enable **AWS WAF** attached to CloudFront or ALB.
2. Configure a **Rate-based Rule** (e.g. limit any single IP address to 100 requests per 5-minute period).
3. Enable AWS Shield Standard / Advanced for automatic Layer 3/4 SYN flood mitigation.

---

## Scenario 11-50 Summary Coverage Matrix
- **OSI vs TCP/IP Models:** Layer 2 Data Link (MAC frames) vs Layer 3 Network (IP packets) vs Layer 4 Transport (TCP segments).
- **VPN & Direct Connect:** IPSec Site-to-Site VPN tunnels, AWS Transit Gateway routing topologies.
- **TLS/SSL Mechanics:** Asymmetric RSA/ECC handshake exchange, symmetric AES session encryption.
