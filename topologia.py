from mininet.topo import Topo


class Topologia(Topo):

    def build(self, n=1):
        # Add hosts
        leftHost1 = self.addHost('lh1', ip="10.10.10.1")
        leftHost2 = self.addHost('lh2', ip="10.10.10.2")
        rightHost1 = self.addHost('rh1', ip="10.10.11.1")
        rightHost2 = self.addHost('rh2', ip="10.10.11.2")

        # Add switches
        switches = []
        for s in range(n):
            switches.append(self.addSwitch('s%s' % (s + 1), dpid="%s" % (s + 1)))
            if s > 0:
                self.addLink(switches[s - 1], switches[s])

        # Add links
        self.addLink(leftHost1, switches[0])
        self.addLink(leftHost2, switches[0])
        self.addLink(switches[n - 1], rightHost1)
        self.addLink(switches[n - 1], rightHost2)


topos = {'mytopo': (lambda: Topologia())}
