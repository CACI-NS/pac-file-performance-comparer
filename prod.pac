function FindProxyForURL(url, host) {
    /* This is an example made-up PAC file to show differences in before and after JavaScript code refactoring */
    var proxy_a = "PROXY 1.1.1.1:8080";
    var proxy_b = "PROXY 2.2.2.2:8080";
    /* Internal Intranet Entries via Direct */
    if(dnsDomainIs(host, ".internal-domain.company.com") ||
	dnsDomainIs(host, ".something-else-old.oldcompanyname.com"))
    return "DIRECT";

    /* Special External Websites via Proxy1 */
    if(shExpMatch(url, "*-specialsite.com"))
    return proxy_a;

    /* Everything else via Proxy2 */
    return proxy_b;
}