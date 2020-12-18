from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto.ofproto_v1_3_parser import OFPSwitchFeatures, OFPPacketIn

from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls

class Hub(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Hub, self).__init__(*args, **kwargs)

    @set_ev_cls(OFPSwitchFeatures, CONFIG_DISPATCHER)
    def handler(self, ev):
        pass
     
    def add_flow(self, datapath, priority, match, actions):
        pass

    @set_ev_cls(OFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser

        print('type of ev is {}, and msg = {}'.format(type(ev), msg))
        
