-- 设备表（自增主键）
CREATE TABLE iot_device (
    id BIGSERIAL PRIMARY KEY,
    device_id VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(128) NOT NULL,
    type VARCHAR(64) NOT NULL,
    status INT NOT NULL DEFAULT 0,
    description VARCHAR(512),
    metadata TEXT,
    last_online TIMESTAMPTZ,
    created_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMPTZ,
    deleted BIGINT NOT NULL DEFAULT 0,
    deleted_time TIMESTAMPTZ
);

COMMENT ON TABLE iot_device IS '物联网设备表';
COMMENT ON COLUMN iot_device.device_id IS '设备唯一标识符';
COMMENT ON COLUMN iot_device.name IS '设备名称';
COMMENT ON COLUMN iot_device.type IS '设备类型';
COMMENT ON COLUMN iot_device.status IS '设备状态（0: 离线, 1: 在线, 2: 异常）';
COMMENT ON COLUMN iot_device.description IS '设备描述';
COMMENT ON COLUMN iot_device.metadata IS '设备元数据 (JSON)';
COMMENT ON COLUMN iot_device.last_online IS '最后在线时间';
COMMENT ON COLUMN iot_device.deleted IS '是否已删除';

-- 设备遥测数据表（自增主键，无逻辑删除）
CREATE TABLE iot_device_data (
    id BIGSERIAL PRIMARY KEY,
    device_id VARCHAR(64) NOT NULL,
    metric_key VARCHAR(128) NOT NULL,
    metric_value TEXT NOT NULL,
    unit VARCHAR(32),
    quality INT,
    created_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE iot_device_data IS '物联网设备遥测数据表';
COMMENT ON COLUMN iot_device_data.device_id IS '设备唯一标识符';
COMMENT ON COLUMN iot_device_data.metric_key IS '指标名称';
COMMENT ON COLUMN iot_device_data.metric_value IS '指标值';
COMMENT ON COLUMN iot_device_data.unit IS '单位';
COMMENT ON COLUMN iot_device_data.quality IS '数据质量';
COMMENT ON COLUMN iot_device_data.created_time IS '数据时间戳';

CREATE INDEX idx_iot_device_data_device_id ON iot_device_data(device_id);
CREATE INDEX idx_iot_device_data_created_time ON iot_device_data(created_time);
CREATE INDEX idx_iot_device_data_metric_key ON iot_device_data(metric_key);
