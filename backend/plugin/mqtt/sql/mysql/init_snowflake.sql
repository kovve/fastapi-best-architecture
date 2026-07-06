-- 设备表（雪花算法主键）
CREATE TABLE iot_device (
    id BIGINT PRIMARY KEY COMMENT '主键 ID',
    device_id VARCHAR(64) NOT NULL UNIQUE COMMENT '设备唯一标识符',
    name VARCHAR(128) NOT NULL COMMENT '设备名称',
    type VARCHAR(64) NOT NULL COMMENT '设备类型',
    status INT NOT NULL DEFAULT 0 COMMENT '设备状态（0: 离线, 1: 在线, 2: 异常）',
    description VARCHAR(512) NULL COMMENT '设备描述',
    metadata LONGTEXT NULL COMMENT '设备元数据 (JSON)',
    last_online DATETIME NULL COMMENT '最后在线时间',
    created_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_time DATETIME NULL COMMENT '更新时间',
    deleted BIGINT NOT NULL DEFAULT 0 COMMENT '是否已删除',
    deleted_time DATETIME NULL COMMENT '删除时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='物联网设备表';

-- 设备遥测数据表（雪花算法主键，无逻辑删除）
CREATE TABLE iot_device_data (
    id BIGINT PRIMARY KEY COMMENT '主键 ID',
    device_id VARCHAR(64) NOT NULL COMMENT '设备唯一标识符',
    metric_key VARCHAR(128) NOT NULL COMMENT '指标名称',
    metric_value LONGTEXT NOT NULL COMMENT '指标值',
    unit VARCHAR(32) NULL COMMENT '单位',
    quality INT NULL COMMENT '数据质量',
    created_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据时间戳'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='物联网设备遥测数据表';

CREATE INDEX idx_iot_device_data_device_id ON iot_device_data(device_id);
CREATE INDEX idx_iot_device_data_created_time ON iot_device_data(created_time);
CREATE INDEX idx_iot_device_data_metric_key ON iot_device_data(metric_key);
