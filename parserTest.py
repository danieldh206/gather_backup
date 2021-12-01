from ntc_templates.parse import parse_output
vlan_output = ("""
Syslog logging: enabled (0 messages dropped, 1 messages rate-limited, 0 flushes, 0 overruns, xml disabled, filtering disabled)

No Active Message Discriminator.



No Inactive Message Discriminator.


    Console logging: disabled
    Monitor logging: level debugging, 0 messages logged, xml disabled,
                     filtering disabled
    Buffer logging:  level debugging, 1808 messages logged, xml disabled,
                    filtering disabled
    Exception Logging: size (4096 bytes)
    Count and timestamp logging messages: disabled
    Persistent logging: disabled

No active filter modules.

    Trap logging: level debugging, 1817 message lines logged
        Logging to 140.142.37.141  (udp port 514, audit disabled,
              link up),
              1814 message lines logged, 
              0 message lines rate-limited, 
              0 message lines dropped-by-MD, 
              xml disabled, sequence number disabled
              filtering disabled
        Logging to 140.142.37.166  (udp port 514, audit disabled,
              link up),
              1817 message lines logged, 
              0 message lines rate-limited, 
              0 message lines dropped-by-MD, 
              xml disabled, sequence number disabled
              filtering disabled
        Logging to 140.142.37.201  (udp port 514, audit disabled,
              link up),
              1817 message lines logged, 
              0 message lines rate-limited, 
              0 message lines dropped-by-MD, 
              xml disabled, sequence number disabled
              filtering disabled
        Logging to 140.142.37.4  (udp port 514, audit disabled,
              link up),
              1595 message lines logged, 
              0 message lines rate-limited, 
              0 message lines dropped-by-MD, 
              xml disabled, sequence number disabled
              filtering disabled
        Logging to 140.142.37.36  (udp port 514, audit disabled,
              link up),
              1593 message lines logged, 
              0 message lines rate-limited, 
              0 message lines dropped-by-MD, 
              xml disabled, sequence number disabled
              filtering disabled
        Logging Source-Interface:       VRF Name:
        Loopback0                       
          
Log Buffer (65536 bytes):
: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:03:11 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:03:11 PDT Thu Jul 22 2021
Jul 22 10:03:15 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:04:31 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:04:31 PDT Thu Jul 22 2021
Jul 22 10:04:35 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:05:15 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:05:15 PDT Thu Jul 22 2021
Jul 22 10:05:19 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:05:40 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:05:40 PDT Thu Jul 22 2021
Jul 22 10:05:44 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:06:31 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:06:31 PDT Thu Jul 22 2021
Jul 22 10:06:35 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:07:55 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:07:55 PDT Thu Jul 22 2021
Jul 22 10:08:00 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:08:14 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:08:14 PDT Thu Jul 22 2021
Jul 22 10:08:18 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:08:53 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:08:53 PDT Thu Jul 22 2021
Jul 22 10:08:58 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:09:16 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:09:16 PDT Thu Jul 22 2021
Jul 22 10:09:21 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:12:39 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:12:39 PDT Thu Jul 22 2021
Jul 22 10:12:43 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:13:07 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:13:07 PDT Thu Jul 22 2021
Jul 22 10:13:11 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:13:52 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:13:52 PDT Thu Jul 22 2021
Jul 22 10:13:56 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:14:46 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:14:46 PDT Thu Jul 22 2021
Jul 22 10:14:50 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:17:52 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:17:52 PDT Thu Jul 22 2021
Jul 22 10:17:56 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:18:26 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:18:26 PDT Thu Jul 22 2021
Jul 22 10:18:30 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:19:32 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:19:32 PDT Thu Jul 22 2021
Jul 22 10:19:36 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:20:09 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:20:09 PDT Thu Jul 22 2021
Jul 22 10:20:13 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:20:32 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:20:32 PDT Thu Jul 22 2021
Jul 22 10:20:36 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:22:55 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:22:55 PDT Thu Jul 22 2021
Jul 22 10:22:59 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:23:30 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:23:30 PDT Thu Jul 22 2021
Jul 22 10:23:34 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:23:53 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:23:53 PDT Thu Jul 22 2021
Jul 22 10:23:57 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:24:18 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:24:18 PDT Thu Jul 22 2021
Jul 22 10:24:22 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:24:42 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:24:42 PDT Thu Jul 22 2021
Jul 22 10:24:46 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:25:02 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:25:02 PDT Thu Jul 22 2021
Jul 22 10:25:06 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:26:03 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:26:03 PDT Thu Jul 22 2021
Jul 22 10:26:07 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:27:42 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:27:42 PDT Thu Jul 22 2021
Jul 22 10:27:46 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:30:31 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:30:31 PDT Thu Jul 22 2021
Jul 22 10:30:36 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:31:33 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:31:33 PDT Thu Jul 22 2021
Jul 22 10:31:38 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:32:47 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:32:47 PDT Thu Jul 22 2021
Jul 22 10:32:51 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:34:42 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:34:42 PDT Thu Jul 22 2021
Jul 22 10:34:46 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:35:23 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:35:23 PDT Thu Jul 22 2021
Jul 22 10:35:27 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:37:05 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:37:05 PDT Thu Jul 22 2021
Jul 22 10:37:10 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 10:37:26 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 10:37:26 PDT Thu Jul 22 2021
Jul 22 10:37:30 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 1(140.142.37.165)
Jul 22 14:18:22 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: johngh] [Source: 140.142.37.165] [localport: 22] at 14:18:22 PDT Thu Jul 22 2021
Jul 22 14:27:17 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:27:17 PDT Thu Jul 22 2021
Jul 22 14:27:21 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:29:10 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:29:10 PDT Thu Jul 22 2021
Jul 22 14:29:16 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:30:37 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:30:37 PDT Thu Jul 22 2021
Jul 22 14:30:43 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:32:29 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:32:29 PDT Thu Jul 22 2021
Jul 22 14:32:33 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:33:22 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:33:22 PDT Thu Jul 22 2021
Jul 22 14:33:26 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:34:07 PDT: %SSH-4-SSH2_UNEXPECTED_MSG: Unexpected message type has arrived. Terminating the connection from 140.142.37.165
Jul 22 14:35:13 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:35:13 PDT Thu Jul 22 2021
Jul 22 14:35:17 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:39:06 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:39:06 PDT Thu Jul 22 2021
Jul 22 14:39:08 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:41:06 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:41:06 PDT Thu Jul 22 2021
Jul 22 14:41:08 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:42:35 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:42:35 PDT Thu Jul 22 2021
Jul 22 14:42:40 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:46:53 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:46:53 PDT Thu Jul 22 2021
Jul 22 14:46:59 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:47:37 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:47:37 PDT Thu Jul 22 2021
Jul 22 14:47:43 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:48:15 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:48:15 PDT Thu Jul 22 2021
Jul 22 14:48:21 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:49:15 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:49:15 PDT Thu Jul 22 2021
Jul 22 14:49:21 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:50:45 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:50:45 PDT Thu Jul 22 2021
Jul 22 14:50:51 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:52:44 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:52:44 PDT Thu Jul 22 2021
Jul 22 14:52:50 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:53:47 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:53:47 PDT Thu Jul 22 2021
Jul 22 14:53:53 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:54:29 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:54:29 PDT Thu Jul 22 2021
Jul 22 14:54:36 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:57:13 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:57:13 PDT Thu Jul 22 2021
Jul 22 14:57:18 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:58:48 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:58:48 PDT Thu Jul 22 2021
Jul 22 14:58:54 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 14:59:28 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 14:59:28 PDT Thu Jul 22 2021
Jul 22 14:59:34 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:00:50 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:00:50 PDT Thu Jul 22 2021
Jul 22 15:00:55 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:23:37 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:23:37 PDT Thu Jul 22 2021
Jul 22 15:23:42 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:24:01 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:24:01 PDT Thu Jul 22 2021
Jul 22 15:24:07 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:26:16 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:26:16 PDT Thu Jul 22 2021
Jul 22 15:26:22 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:30:23 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:30:23 PDT Thu Jul 22 2021
Jul 22 15:30:29 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:32:11 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:32:11 PDT Thu Jul 22 2021
Jul 22 15:32:14 PDT: %SYS-5-CONFIG_I: Configured from console by danieldh on vty1 (140.142.37.165)
Jul 22 15:32:18 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:43:02 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:43:02 PDT Thu Jul 22 2021
Jul 22 15:44:22 PDT: %SYS-5-CONFIG_I: Configured from console by danieldh on vty1 (140.142.37.165)
Jul 22 15:46:26 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:49:22 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:49:22 PDT Thu Jul 22 2021
Jul 22 15:49:27 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:50:01 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:50:01 PDT Thu Jul 22 2021
Jul 22 15:50:29 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:55:39 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:55:39 PDT Thu Jul 22 2021
Jul 22 15:55:45 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 15:57:37 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 15:57:37 PDT Thu Jul 22 2021
Jul 22 15:59:39 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:01:47 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:01:47 PDT Thu Jul 22 2021
Jul 22 16:01:50 PDT: %SYS-5-CONFIG_I: Configured from console by danieldh on vty1 (140.142.37.165)
Jul 22 16:01:54 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:02:51 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:02:51 PDT Thu Jul 22 2021
Jul 22 16:03:41 PDT: %SYS-5-CONFIG_I: Configured from console by danieldh on vty1 (140.142.37.165)
Jul 22 16:04:03 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:04:09 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:04:09 PDT Thu Jul 22 2021
Jul 22 16:04:12 PDT: %SYS-5-CONFIG_I: Configured from console by danieldh on vty1 (140.142.37.165)
Jul 22 16:04:16 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:10:32 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:10:32 PDT Thu Jul 22 2021
Jul 22 16:11:11 PDT: %SYS-5-CONFIG_I: Configured from console by danieldh on vty1 (140.142.37.165)
Jul 22 16:11:27 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:11:43 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:11:43 PDT Thu Jul 22 2021
Jul 22 16:11:46 PDT: %SYS-5-CONFIG_I: Configured from console by danieldh on vty1 (140.142.37.165)
Jul 22 16:11:50 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:16:07 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:16:07 PDT Thu Jul 22 2021
Jul 22 16:16:13 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:16:44 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:16:44 PDT Thu Jul 22 2021
Jul 22 16:16:50 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:17:37 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:17:37 PDT Thu Jul 22 2021
Jul 22 16:17:43 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:18:34 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:18:34 PDT Thu Jul 22 2021
Jul 22 16:18:39 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:20:18 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:20:18 PDT Thu Jul 22 2021
Jul 22 16:20:24 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:21:52 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:21:52 PDT Thu Jul 22 2021
Jul 22 16:21:58 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:24:30 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:24:30 PDT Thu Jul 22 2021
Jul 22 16:24:36 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:25:19 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:25:19 PDT Thu Jul 22 2021
Jul 22 16:25:25 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:26:29 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:26:29 PDT Thu Jul 22 2021
Jul 22 16:26:34 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:27:59 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:27:59 PDT Thu Jul 22 2021
Jul 22 16:28:04 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:29:37 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 16:29:37 PDT Thu Jul 22 2021
Jul 22 16:29:54 PDT: %SYS-6-LOGOUT: User danieldh has exited tty session 2(140.142.37.165)
Jul 22 16:42:49 PDT: %SYS-6-TTY_EXPIRE_TIMER: (exec timer expired, tty 1 (140.142.37.165)), user johngh
Jul 22 16:42:49 PDT: %SYS-6-LOGOUT: User johngh has exited tty session 1(140.142.37.165)
Jul 22 16:42:49 PDT: %SYS-5-CONFIG_I: Configured from console by johngh on vty0 (140.142.37.165)
Jul 23 15:39:38 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: limdaug] [Source: 140.142.37.165] [localport: 22] at 15:39:38 PDT Fri Jul 23 2021
Jul 23 15:40:14 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 15:40:22 PDT: %SYS-6-LOGOUT: User limdaug has exited tty session 1(140.142.37.165)
Jul 23 15:40:30 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: limdaug] [Source: 140.142.37.165] [localport: 22] at 15:40:30 PDT Fri Jul 23 2021
Jul 23 15:40:59 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 15:49:23 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 15:50:22 PDT: Rollback:Acquired Configuration lock.
Jul 23 15:50:22 PDT: %SYS-5-CONFIG_R: Config Replace is Done
Jul 23 15:50:23 PDT: % Multiple self signed certificates in config
    certificate for trust point TP-self-signed-3203070232 ignored

Jul 23 15:50:24 PDT: % Multiple self signed certificates in config
    certificate for trust point TP-self-signed-3203070232 ignored

Jul 23 15:50:25 PDT: % Multiple self signed certificates in config
    certificate for trust point TP-self-signed-3203070232 ignored

Jul 23 15:50:25 PDT: % Multiple self signed certificates in config
    certificate for trust point TP-self-signed-3203070232 ignored

Jul 23 15:50:26 PDT: % Multiple self signed certificates in config
    certificate for trust point TP-self-signed-3203070232 ignored

Jul 23 15:52:05 PDT: Rollback:Acquired Configuration lock.
Jul 23 15:52:05 PDT: %SYS-5-CONFIG_R: Config Replace is Done
Jul 23 16:06:07 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 16:06:34 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 16:07:06 PDT: Rollback:Acquired Configuration lock.
Jul 23 16:07:06 PDT: %SYS-5-CONFIG_R: Config Replace is Done
Jul 23 16:07:30 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: limdaug] [Source: 140.142.37.165] [localport: 22] at 16:07:30 PDT Fri Jul 23 2021
Jul 23 16:07:31 PDT: %SYS-6-LOGOUT: User limdaug has exited tty session 2(140.142.37.165)
Jul 23 16:12:37 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 16:12:37 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 16:13:25 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 16:13:25 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 16:13:25 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 16:15:11 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 16:15:11 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 16:15:12 PDT: %SYS-5-CONFIG_I: Configured from console by limdaug on vty0 (140.142.37.165)
Jul 23 17:07:03 PDT: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: danieldh] [Source: 140.142.37.165] [localport: 22] at 17:07:03 PDT Fri Jul 23 2021
Jul 23 17:10:42 PDT: %SYS-5-CONFIG_I: Configured from console by danieldh on vty1 (140.142.37.165)
Jul 23 17:11:00 PDT: Rollback:Acquired Configuration lock.
Jul 23 17:11:00 PDT: %SYS-5-CONFIG_R: Config Replace is Done
Jul 23 17:11:01 PDT: % Multiple self signed certificates in config
""")
vlan_parsed = parse_output(platform="cisco_ios", command="show logging", data=vlan_output)
for line in vlan_parsed:
    print (line)
