create database if not exists system_monitor;
USE system_monitor;

create table metrics (
    id tinyint auto_increment primary key,
    timestamp datetime default current_timestamp,
    cpu_usage float,
    memory_usage float,
    disk_usage float,
    disk_read_mb float,
    disk_write_mb float,
    disk_read_count int,
    disk_write_count int,
    net_sent_mb float,
    net_resv_mb float,
    index idx_timestamp (timestamp)
) engine=InnoDB default charset=utf8mb4;
