{application, rabbit,           %% -*- erlang -*-
 [{description, "RabbitMQ"},
  {id, "RabbitMQ"},
  {vsn, "3.6.6"},
  {modules, ['background_gc','delegate','delegate_sup','dtree','file_handle_cache','file_handle_cache_stats','gatherer','gm','lqueue','mirrored_supervisor_sups','mnesia_sync','pg_local','rabbit','rabbit_access_control','rabbit_alarm','rabbit_amqqueue_process','rabbit_amqqueue_sup','rabbit_amqqueue_sup_sup','rabbit_auth_mechanism_amqplain','rabbit_auth_mechanism_cr_demo','rabbit_auth_mechanism_plain','rabbit_autoheal','rabbit_binding','rabbit_boot_steps','rabbit_channel_sup','rabbit_channel_sup_sup','rabbit_cli','rabbit_client_sup','rabbit_connection_helper_sup','rabbit_connection_sup','rabbit_control_main','rabbit_control_pbe','rabbit_ctl_usage','rabbit_dead_letter','rabbit_diagnostics','rabbit_direct','rabbit_disk_monitor','rabbit_epmd_monitor','rabbit_error_logger','rabbit_error_logger_file_h','rabbit_exchange','rabbit_exchange_parameters','rabbit_exchange_type_direct','rabbit_exchange_type_fanout','rabbit_exchange_type_headers','rabbit_exchange_type_invalid','rabbit_exchange_type_topic','rabbit_file','rabbit_framing','rabbit_guid','rabbit_hipe','rabbit_limiter','rabbit_log','rabbit_memory_monitor','rabbit_mirror_queue_coordinator','rabbit_mirror_queue_master','rabbit_mirror_queue_misc','rabbit_mirror_queue_mode','rabbit_mirror_queue_mode_all','rabbit_mirror_queue_mode_exactly','rabbit_mirror_queue_mode_nodes','rabbit_mirror_queue_slave','rabbit_mirror_queue_sync','rabbit_mnesia','rabbit_mnesia_rename','rabbit_msg_file','rabbit_msg_store','rabbit_msg_store_ets_index','rabbit_msg_store_gc','rabbit_node_monitor','rabbit_parameter_validation','rabbit_password','rabbit_password_hashing_md5','rabbit_password_hashing_sha256','rabbit_password_hashing_sha512','rabbit_pbe','rabbit_plugins','rabbit_plugins_main','rabbit_plugins_usage','rabbit_policies','rabbit_policy','rabbit_prelaunch','rabbit_prequeue','rabbit_priority_queue','rabbit_queue_consumers','rabbit_queue_index','rabbit_queue_location_client_local','rabbit_queue_location_min_masters','rabbit_queue_location_random','rabbit_queue_location_validator','rabbit_queue_master_location_misc','rabbit_recovery_terms','rabbit_registry','rabbit_resource_monitor_misc','rabbit_restartable_sup','rabbit_router','rabbit_runtime_parameters','rabbit_sasl_report_file_h','rabbit_ssl','rabbit_sup','rabbit_table','rabbit_trace','rabbit_upgrade','rabbit_upgrade_functions','rabbit_variable_queue','rabbit_version','rabbit_vhost','rabbit_vm','supervised_lifecycle','tcp_listener','tcp_listener_sup','truncate','vm_memory_monitor','worker_pool','worker_pool_sup','worker_pool_worker']},
  {registered, [rabbit_amqqueue_sup,
                rabbit_log,
                rabbit_node_monitor,
                rabbit_router,
                rabbit_sup,
                rabbit_direct_client_sup]},
  {applications, [kernel, stdlib, sasl, mnesia, rabbit_common, ranch, os_mon, xmerl]},
%% we also depend on crypto, public_key and ssl but they shouldn't be
%% in here as we don't actually want to start it
  {mod, {rabbit, []}},
  {env, [{tcp_listeners, [5672]},
         {num_tcp_acceptors, 10},
         {ssl_listeners, []},
         {num_ssl_acceptors, 1},
         {ssl_options, []},
         {vm_memory_high_watermark, 0.4},
         {vm_memory_high_watermark_paging_ratio, 0.5},
         {memory_monitor_interval, 2500},
         {disk_free_limit, 50000000}, %% 50MB
         {msg_store_index_module, rabbit_msg_store_ets_index},
         {backing_queue_module, rabbit_variable_queue},
         %% 0 ("no limit") would make a better default, but that
         %% breaks the QPid Java client
         {frame_max, 131072},
         {channel_max, 0},
         {heartbeat, 60},
         {msg_store_file_size_limit, 16777216},
         {fhc_write_buffering, true},
         {fhc_read_buffering, false},
         {queue_index_max_journal_entries, 32768},
         {queue_index_embed_msgs_below, 4096},
         {default_user, <<"guest">>},
         {default_pass, <<"guest">>},
         {default_user_tags, [administrator]},
         {default_vhost, <<"/">>},
         {default_permissions, [<<".*">>, <<".*">>, <<".*">>]},
         {loopback_users, [<<"guest">>]},
         {password_hashing_module, rabbit_password_hashing_sha256},
         {cluster_nodes, {[], disc}},
         {server_properties, []},
         {collect_statistics, none},
         {collect_statistics_interval, 5000},
         {mnesia_table_loading_timeout, 30000},
         {auth_mechanisms, ['PLAIN', 'AMQPLAIN']},
         {auth_backends, [rabbit_auth_backend_internal]},
         {delegate_count, 16},
         {trace_vhosts, []},
         {log_levels, [{connection, info}]},
         {ssl_cert_login_from, distinguished_name},
         {ssl_handshake_timeout, 5000},
         {ssl_allow_poodle_attack, false},
         {handshake_timeout, 10000},
         {reverse_dns_lookups, false},
         {cluster_partition_handling, ignore},
         {cluster_keepalive_interval, 10000},
         {tcp_listen_options, [{backlog,       128},
                               {nodelay,       true},
                               {linger,        {true, 0}},
                               {exit_on_close, false}]},
         {halt_on_upgrade_failure, true},
         {hipe_compile, false},
         %% see bug 24513 for how this list was created
         {hipe_modules,
          [rabbit_reader, rabbit_channel, gen_server2, rabbit_exchange,
           rabbit_command_assembler, rabbit_framing_amqp_0_9_1, rabbit_basic,
           rabbit_event, lists, queue, priority_queue, rabbit_router,
           rabbit_trace, rabbit_misc, rabbit_binary_parser,
           rabbit_exchange_type_direct, rabbit_guid, rabbit_net,
           rabbit_amqqueue_process, rabbit_variable_queue,
           rabbit_binary_generator, rabbit_writer, delegate, gb_sets, lqueue,
           sets, orddict, rabbit_amqqueue, rabbit_limiter, gb_trees,
           rabbit_queue_index, rabbit_exchange_decorator, gen, dict, ordsets,
           file_handle_cache, rabbit_msg_store, array,
           rabbit_msg_store_ets_index, rabbit_msg_file,
           rabbit_exchange_type_fanout, rabbit_exchange_type_topic, mnesia,
           mnesia_lib, rpc, mnesia_tm, qlc, sofs, proplists, credit_flow,
           pmon, ssl_connection, tls_connection, ssl_record, tls_record,
           gen_fsm, ssl]},
         {ssl_apps, [asn1, crypto, public_key, ssl]},
         %% see rabbitmq-server#114
         {mirroring_flow_control, true},
         {mirroring_sync_batch_size, 4096},
         %% see rabbitmq-server#227 and related tickets.
         %% msg_store_credit_disc_bound only takes effect when
         %% messages are persisted to the message store. If messages
         %% are embedded on the queue index, then modifying this
         %% setting has no effect because credit_flow is not used when
         %% writing to the queue index. See the setting
         %% queue_index_embed_msgs_below above.
         {msg_store_credit_disc_bound, {2000, 500}},
         {msg_store_io_batch_size, 2048},
         %% see rabbitmq-server#143
         %% and rabbitmq-server#949
         {credit_flow_default_credit, {200, 100}},
         %% see rabbitmq-server#248
         %% and rabbitmq-server#667
         {channel_operation_timeout, 15000},
         {config_entry_decoder, [
             {cipher, aes_cbc256},
             {hash, sha512},
             {iterations, 1000},
             {passphrase, undefined}
         ]},
         %% rabbitmq-server-973
         {lazy_queue_explicit_gc_run_operation_threshold, 250}
        ]}]}.
