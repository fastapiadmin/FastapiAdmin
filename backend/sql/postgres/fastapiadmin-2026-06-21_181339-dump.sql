--
-- PostgreSQL database dump
--

\restrict qwiwcp7I4gdDmIy1kyj9QBOQCzllutf9XAPaoJPcYOFGDJwS41ngMgrWMeUHoPW

-- Dumped from database version 17.5 (ServBay)
-- Dumped by pg_dump version 18.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: apscheduler_jobs; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.apscheduler_jobs (
    id character varying(191) NOT NULL,
    next_run_time double precision,
    job_state bytea NOT NULL
);


ALTER TABLE public.apscheduler_jobs OWNER TO root;

--
-- Name: example_demo; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.example_demo (
    name character varying(64) NOT NULL,
    status integer NOT NULL,
    description text,
    int_val integer,
    bigint_val bigint,
    float_val double precision,
    bool_val boolean NOT NULL,
    date_val date,
    time_val time without time zone,
    datetime_val timestamp without time zone,
    text_val text,
    json_val json,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.example_demo OWNER TO root;

--
-- Name: TABLE example_demo; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.example_demo IS '示例表';


--
-- Name: COLUMN example_demo.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.name IS '名称';


--
-- Name: COLUMN example_demo.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN example_demo.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.description IS '备注';


--
-- Name: COLUMN example_demo.int_val; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.int_val IS '整数';


--
-- Name: COLUMN example_demo.bigint_val; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.bigint_val IS '大整数';


--
-- Name: COLUMN example_demo.float_val; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.float_val IS '浮点数';


--
-- Name: COLUMN example_demo.bool_val; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.bool_val IS '布尔型';


--
-- Name: COLUMN example_demo.date_val; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.date_val IS '日期';


--
-- Name: COLUMN example_demo.time_val; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.time_val IS '时间';


--
-- Name: COLUMN example_demo.datetime_val; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.datetime_val IS '日期时间';


--
-- Name: COLUMN example_demo.text_val; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.text_val IS '长文本';


--
-- Name: COLUMN example_demo.json_val; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.json_val IS '元数据(JSON格式)';


--
-- Name: COLUMN example_demo.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.id IS '主键ID';


--
-- Name: COLUMN example_demo.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN example_demo.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN example_demo.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.created_time IS '创建时间';


--
-- Name: COLUMN example_demo.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.updated_time IS '更新时间';


--
-- Name: COLUMN example_demo.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.deleted_time IS '删除时间';


--
-- Name: COLUMN example_demo.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.tenant_id IS '租户ID';


--
-- Name: COLUMN example_demo.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.created_id IS '创建人ID';


--
-- Name: COLUMN example_demo.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.updated_id IS '更新人ID';


--
-- Name: COLUMN example_demo.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.example_demo.deleted_id IS '删除人ID';


--
-- Name: example_demo_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.example_demo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.example_demo_id_seq OWNER TO root;

--
-- Name: example_demo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.example_demo_id_seq OWNED BY public.example_demo.id;


--
-- Name: gen_table; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.gen_table (
    table_name character varying(200) NOT NULL,
    table_comment character varying(500),
    class_name character varying(100) NOT NULL,
    package_name character varying(100),
    module_name character varying(30),
    business_name character varying(30),
    function_name character varying(100),
    sub_table_name character varying(64) DEFAULT NULL::character varying,
    sub_table_fk_name character varying(64) DEFAULT NULL::character varying,
    parent_menu_id integer,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.gen_table OWNER TO root;

--
-- Name: TABLE gen_table; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.gen_table IS '代码生成表';


--
-- Name: COLUMN gen_table.table_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.table_name IS '表名称';


--
-- Name: COLUMN gen_table.table_comment; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.table_comment IS '表描述';


--
-- Name: COLUMN gen_table.class_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.class_name IS '实体类名称';


--
-- Name: COLUMN gen_table.package_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.package_name IS '生成包路径';


--
-- Name: COLUMN gen_table.module_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.module_name IS '生成模块名';


--
-- Name: COLUMN gen_table.business_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.business_name IS '生成业务名';


--
-- Name: COLUMN gen_table.function_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.function_name IS '生成功能名';


--
-- Name: COLUMN gen_table.sub_table_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.sub_table_name IS '关联子表的表名';


--
-- Name: COLUMN gen_table.sub_table_fk_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.sub_table_fk_name IS '子表关联的外键名';


--
-- Name: COLUMN gen_table.parent_menu_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.parent_menu_id IS '父菜单ID';


--
-- Name: COLUMN gen_table.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN gen_table.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.description IS '备注';


--
-- Name: COLUMN gen_table.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.id IS '主键ID';


--
-- Name: COLUMN gen_table.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_table.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN gen_table.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.created_time IS '创建时间';


--
-- Name: COLUMN gen_table.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.updated_time IS '更新时间';


--
-- Name: COLUMN gen_table.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.deleted_time IS '删除时间';


--
-- Name: COLUMN gen_table.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.tenant_id IS '租户ID';


--
-- Name: COLUMN gen_table.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.created_id IS '创建人ID';


--
-- Name: COLUMN gen_table.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.updated_id IS '更新人ID';


--
-- Name: COLUMN gen_table.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.deleted_id IS '删除人ID';


--
-- Name: gen_table_column; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.gen_table_column (
    column_name character varying(200) NOT NULL,
    column_comment character varying(500),
    column_type character varying(100) NOT NULL,
    column_length character varying(50),
    column_default character varying(200),
    is_pk boolean DEFAULT false NOT NULL,
    is_increment boolean DEFAULT false NOT NULL,
    is_nullable boolean DEFAULT true NOT NULL,
    is_unique boolean DEFAULT false NOT NULL,
    python_type character varying(100),
    python_field character varying(200),
    is_insert boolean DEFAULT true NOT NULL,
    is_edit boolean DEFAULT true NOT NULL,
    is_list boolean DEFAULT true NOT NULL,
    is_query boolean DEFAULT false NOT NULL,
    query_type character varying(50),
    html_type character varying(100),
    dict_type character varying(200),
    sort integer NOT NULL,
    table_id integer NOT NULL,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.gen_table_column OWNER TO root;

--
-- Name: TABLE gen_table_column; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.gen_table_column IS '代码生成表字段';


--
-- Name: COLUMN gen_table_column.column_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.column_name IS '列名称';


--
-- Name: COLUMN gen_table_column.column_comment; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.column_comment IS '列描述';


--
-- Name: COLUMN gen_table_column.column_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.column_type IS '列类型';


--
-- Name: COLUMN gen_table_column.column_length; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.column_length IS '列长度';


--
-- Name: COLUMN gen_table_column.column_default; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.column_default IS '列默认值';


--
-- Name: COLUMN gen_table_column.is_pk; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.is_pk IS '是否主键';


--
-- Name: COLUMN gen_table_column.is_increment; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.is_increment IS '是否自增';


--
-- Name: COLUMN gen_table_column.is_nullable; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.is_nullable IS '是否允许为空';


--
-- Name: COLUMN gen_table_column.is_unique; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.is_unique IS '是否唯一';


--
-- Name: COLUMN gen_table_column.python_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.python_type IS 'Python类型';


--
-- Name: COLUMN gen_table_column.python_field; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.python_field IS 'Python字段名';


--
-- Name: COLUMN gen_table_column.is_insert; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.is_insert IS '是否为新增字段';


--
-- Name: COLUMN gen_table_column.is_edit; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.is_edit IS '是否编辑字段';


--
-- Name: COLUMN gen_table_column.is_list; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.is_list IS '是否列表字段';


--
-- Name: COLUMN gen_table_column.is_query; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.is_query IS '是否查询字段';


--
-- Name: COLUMN gen_table_column.query_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.query_type IS '查询方式';


--
-- Name: COLUMN gen_table_column.html_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.html_type IS '前端显示类型';


--
-- Name: COLUMN gen_table_column.dict_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.dict_type IS '前端对应字典类型';


--
-- Name: COLUMN gen_table_column.sort; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.sort IS '排序';


--
-- Name: COLUMN gen_table_column.table_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.table_id IS '归属表编号';


--
-- Name: COLUMN gen_table_column.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN gen_table_column.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.description IS '备注';


--
-- Name: COLUMN gen_table_column.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.id IS '主键ID';


--
-- Name: COLUMN gen_table_column.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_table_column.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN gen_table_column.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.created_time IS '创建时间';


--
-- Name: COLUMN gen_table_column.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.updated_time IS '更新时间';


--
-- Name: COLUMN gen_table_column.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.deleted_time IS '删除时间';


--
-- Name: COLUMN gen_table_column.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.tenant_id IS '租户ID';


--
-- Name: COLUMN gen_table_column.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.created_id IS '创建人ID';


--
-- Name: COLUMN gen_table_column.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.updated_id IS '更新人ID';


--
-- Name: COLUMN gen_table_column.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.deleted_id IS '删除人ID';


--
-- Name: gen_table_column_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.gen_table_column_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_table_column_id_seq OWNER TO root;

--
-- Name: gen_table_column_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.gen_table_column_id_seq OWNED BY public.gen_table_column.id;


--
-- Name: gen_table_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.gen_table_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_table_id_seq OWNER TO root;

--
-- Name: gen_table_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.gen_table_id_seq OWNED BY public.gen_table.id;


--
-- Name: platform_email_config; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_email_config (
    name character varying(100) NOT NULL,
    smtp_host character varying(255) NOT NULL,
    smtp_port integer NOT NULL,
    smtp_user character varying(255) NOT NULL,
    smtp_password character varying(255) NOT NULL,
    from_name character varying(100) NOT NULL,
    use_tls boolean NOT NULL,
    is_default boolean NOT NULL,
    timeout integer NOT NULL,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone
);


ALTER TABLE public.platform_email_config OWNER TO root;

--
-- Name: TABLE platform_email_config; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_email_config IS '邮件 SMTP 配置表';


--
-- Name: COLUMN platform_email_config.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.name IS '配置名称';


--
-- Name: COLUMN platform_email_config.smtp_host; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.smtp_host IS 'SMTP 服务器地址';


--
-- Name: COLUMN platform_email_config.smtp_port; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.smtp_port IS 'SMTP 端口（465=SSL, 587=TLS）';


--
-- Name: COLUMN platform_email_config.smtp_user; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.smtp_user IS 'SMTP 登录用户名（发件邮箱）';


--
-- Name: COLUMN platform_email_config.smtp_password; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.smtp_password IS 'SMTP 授权密码（AES 加密存储）';


--
-- Name: COLUMN platform_email_config.from_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.from_name IS '发件人显示名';


--
-- Name: COLUMN platform_email_config.use_tls; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.use_tls IS '是否启用 SSL/TLS';


--
-- Name: COLUMN platform_email_config.is_default; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.is_default IS '是否为默认配置';


--
-- Name: COLUMN platform_email_config.timeout; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.timeout IS '连接超时（秒）';


--
-- Name: COLUMN platform_email_config.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN platform_email_config.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.description IS '备注';


--
-- Name: COLUMN platform_email_config.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.id IS '主键ID';


--
-- Name: COLUMN platform_email_config.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_email_config.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_email_config.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.created_time IS '创建时间';


--
-- Name: COLUMN platform_email_config.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.updated_time IS '更新时间';


--
-- Name: COLUMN platform_email_config.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_config.deleted_time IS '删除时间';


--
-- Name: platform_email_config_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_email_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_email_config_id_seq OWNER TO root;

--
-- Name: platform_email_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_email_config_id_seq OWNED BY public.platform_email_config.id;


--
-- Name: platform_email_log; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_email_log (
    config_id integer,
    template_code character varying(100),
    to_email character varying(255) NOT NULL,
    to_name character varying(100),
    subject character varying(255) NOT NULL,
    biz_type character varying(50) NOT NULL,
    error_msg text,
    retry_count integer NOT NULL,
    tenant_id integer,
    sent_time timestamp without time zone,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.platform_email_log OWNER TO root;

--
-- Name: TABLE platform_email_log; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_email_log IS '邮件发送日志表';


--
-- Name: COLUMN platform_email_log.config_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.config_id IS '使用的 SMTP 配置 ID';


--
-- Name: COLUMN platform_email_log.template_code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.template_code IS '模板编码（冗余存储，模板删除后仍可追溯）';


--
-- Name: COLUMN platform_email_log.to_email; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.to_email IS '收件人邮箱';


--
-- Name: COLUMN platform_email_log.to_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.to_name IS '收件人姓名';


--
-- Name: COLUMN platform_email_log.subject; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.subject IS '邮件主题（渲染后）';


--
-- Name: COLUMN platform_email_log.biz_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.biz_type IS '业务类型（register/reset_password/invite/expiry_warning/ticket_reply/other）';


--
-- Name: COLUMN platform_email_log.error_msg; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.error_msg IS '失败原因';


--
-- Name: COLUMN platform_email_log.retry_count; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.retry_count IS '重试次数';


--
-- Name: COLUMN platform_email_log.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.tenant_id IS '关联租户 ID（可为空，如平台注册邮件）';


--
-- Name: COLUMN platform_email_log.sent_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.sent_time IS '实际发送时间';


--
-- Name: COLUMN platform_email_log.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN platform_email_log.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.description IS '备注';


--
-- Name: COLUMN platform_email_log.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.id IS '主键ID';


--
-- Name: COLUMN platform_email_log.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_email_log.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_email_log.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.created_time IS '创建时间';


--
-- Name: COLUMN platform_email_log.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.updated_time IS '更新时间';


--
-- Name: COLUMN platform_email_log.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.deleted_time IS '删除时间';


--
-- Name: COLUMN platform_email_log.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.created_id IS '创建人ID';


--
-- Name: COLUMN platform_email_log.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.updated_id IS '更新人ID';


--
-- Name: COLUMN platform_email_log.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_log.deleted_id IS '删除人ID';


--
-- Name: platform_email_log_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_email_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_email_log_id_seq OWNER TO root;

--
-- Name: platform_email_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_email_log_id_seq OWNED BY public.platform_email_log.id;


--
-- Name: platform_email_template; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_email_template (
    name character varying(100) NOT NULL,
    template_code character varying(100) NOT NULL,
    subject character varying(255) NOT NULL,
    body_html text NOT NULL,
    body_text text,
    variables text,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone
);


ALTER TABLE public.platform_email_template OWNER TO root;

--
-- Name: TABLE platform_email_template; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_email_template IS '邮件模板表';


--
-- Name: COLUMN platform_email_template.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.name IS '模板名称';


--
-- Name: COLUMN platform_email_template.template_code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.template_code IS '模板编码（业务键）';


--
-- Name: COLUMN platform_email_template.subject; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.subject IS '邮件主题（可含变量）';


--
-- Name: COLUMN platform_email_template.body_html; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.body_html IS '邮件正文 HTML（Jinja2 模板）';


--
-- Name: COLUMN platform_email_template.body_text; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.body_text IS '邮件纯文本版本（降级用）';


--
-- Name: COLUMN platform_email_template.variables; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.variables IS '模板变量说明（JSON 格式，如 {"username": "用户名", "link": "链接"}）';


--
-- Name: COLUMN platform_email_template.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN platform_email_template.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.description IS '备注';


--
-- Name: COLUMN platform_email_template.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.id IS '主键ID';


--
-- Name: COLUMN platform_email_template.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_email_template.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_email_template.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.created_time IS '创建时间';


--
-- Name: COLUMN platform_email_template.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.updated_time IS '更新时间';


--
-- Name: COLUMN platform_email_template.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_email_template.deleted_time IS '删除时间';


--
-- Name: platform_email_template_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_email_template_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_email_template_id_seq OWNER TO root;

--
-- Name: platform_email_template_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_email_template_id_seq OWNED BY public.platform_email_template.id;


--
-- Name: platform_invoice; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_invoice (
    invoice_no character varying(32) NOT NULL,
    order_id integer NOT NULL,
    invoice_type character varying(20) NOT NULL,
    title character varying(200) NOT NULL,
    tax_no character varying(50),
    bank_info text,
    address_info text,
    amount integer NOT NULL,
    tax_amount integer NOT NULL,
    pdf_url character varying(500),
    oss_license_pdf_url character varying(500),
    api_response text,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.platform_invoice OWNER TO root;

--
-- Name: TABLE platform_invoice; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_invoice IS '发票表';


--
-- Name: COLUMN platform_invoice.invoice_no; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.invoice_no IS '发票号码';


--
-- Name: COLUMN platform_invoice.order_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.order_id IS '关联订单';


--
-- Name: COLUMN platform_invoice.invoice_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.invoice_type IS 'vat_normal/vat_special';


--
-- Name: COLUMN platform_invoice.title; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.title IS '发票抬头';


--
-- Name: COLUMN platform_invoice.tax_no; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.tax_no IS '纳税人识别号';


--
-- Name: COLUMN platform_invoice.bank_info; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.bank_info IS '开户行及账号';


--
-- Name: COLUMN platform_invoice.address_info; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.address_info IS '注册地址及电话';


--
-- Name: COLUMN platform_invoice.amount; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.amount IS '发票金额(分)';


--
-- Name: COLUMN platform_invoice.tax_amount; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.tax_amount IS '税额(分)';


--
-- Name: COLUMN platform_invoice.pdf_url; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.pdf_url IS '发票PDF下载地址';


--
-- Name: COLUMN platform_invoice.oss_license_pdf_url; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.oss_license_pdf_url IS '开源授权函PDF下载地址';


--
-- Name: COLUMN platform_invoice.api_response; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.api_response IS '第三方API响应';


--
-- Name: COLUMN platform_invoice.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.status IS '状态(0:待开票 1:已开票 2:开票失败 3:已作废)';


--
-- Name: COLUMN platform_invoice.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.description IS '备注';


--
-- Name: COLUMN platform_invoice.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.id IS '主键ID';


--
-- Name: COLUMN platform_invoice.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_invoice.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_invoice.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.created_time IS '创建时间';


--
-- Name: COLUMN platform_invoice.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.updated_time IS '更新时间';


--
-- Name: COLUMN platform_invoice.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.deleted_time IS '删除时间';


--
-- Name: COLUMN platform_invoice.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.tenant_id IS '租户ID';


--
-- Name: COLUMN platform_invoice.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.created_id IS '创建人ID';


--
-- Name: COLUMN platform_invoice.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.updated_id IS '更新人ID';


--
-- Name: COLUMN platform_invoice.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_invoice.deleted_id IS '删除人ID';


--
-- Name: platform_invoice_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_invoice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_invoice_id_seq OWNER TO root;

--
-- Name: platform_invoice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_invoice_id_seq OWNED BY public.platform_invoice.id;


--
-- Name: platform_menu; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_menu (
    name character varying(50) NOT NULL,
    type integer NOT NULL,
    "order" integer NOT NULL,
    permission character varying(100),
    icon character varying(50),
    route_name character varying(100),
    route_path character varying(200),
    component_path character varying(200),
    redirect character varying(200),
    hidden boolean NOT NULL,
    keep_alive boolean NOT NULL,
    always_show boolean NOT NULL,
    title character varying(50),
    params json,
    affix boolean NOT NULL,
    client character varying(20) DEFAULT 'pc'::character varying NOT NULL,
    link character varying(500),
    is_iframe boolean NOT NULL,
    is_hide_tab boolean NOT NULL,
    active_path character varying(200),
    show_badge boolean NOT NULL,
    show_text_badge character varying(20),
    scope character varying(20) DEFAULT 'tenant'::character varying NOT NULL,
    status integer NOT NULL,
    description text,
    parent_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone
);


ALTER TABLE public.platform_menu OWNER TO root;

--
-- Name: TABLE platform_menu; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_menu IS '平台菜单表';


--
-- Name: COLUMN platform_menu.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.name IS '菜单名称';


--
-- Name: COLUMN platform_menu.type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.type IS '菜单类型(1:目录 2:菜单 3:按钮 4:链接)';


--
-- Name: COLUMN platform_menu."order"; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu."order" IS '显示排序';


--
-- Name: COLUMN platform_menu.permission; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.permission IS '权限标识(如:module_system:user:query)';


--
-- Name: COLUMN platform_menu.icon; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.icon IS '菜单图标';


--
-- Name: COLUMN platform_menu.route_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.route_name IS '路由名称';


--
-- Name: COLUMN platform_menu.route_path; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.route_path IS '路由路径';


--
-- Name: COLUMN platform_menu.component_path; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.component_path IS '组件路径';


--
-- Name: COLUMN platform_menu.redirect; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.redirect IS '重定向地址';


--
-- Name: COLUMN platform_menu.hidden; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.hidden IS '是否隐藏(True:隐藏 False:显示)';


--
-- Name: COLUMN platform_menu.keep_alive; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.keep_alive IS '是否缓存(True:是 False:否)';


--
-- Name: COLUMN platform_menu.always_show; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.always_show IS '是否始终显示(True:是 False:否)';


--
-- Name: COLUMN platform_menu.title; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.title IS '菜单标题';


--
-- Name: COLUMN platform_menu.params; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.params IS '路由参数(JSON对象)';


--
-- Name: COLUMN platform_menu.affix; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.affix IS '是否固定标签页(True:是 False:否)';


--
-- Name: COLUMN platform_menu.client; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.client IS '终端(pc:管理端桌面 app:移动端)';


--
-- Name: COLUMN platform_menu.link; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.link IS '外链地址(仅type=4)';


--
-- Name: COLUMN platform_menu.is_iframe; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.is_iframe IS '是否嵌入iframe(True:是 False:否)';


--
-- Name: COLUMN platform_menu.is_hide_tab; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.is_hide_tab IS '是否隐藏标签页(True:是 False:否)';


--
-- Name: COLUMN platform_menu.active_path; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.active_path IS '激活菜单路径(用于高亮父级)';


--
-- Name: COLUMN platform_menu.show_badge; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.show_badge IS '是否显示红点角标(True:是 False:否)';


--
-- Name: COLUMN platform_menu.show_text_badge; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.show_text_badge IS '文字角标内容';


--
-- Name: COLUMN platform_menu.scope; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.scope IS '菜单可见范围(platform:仅平台 tenant:租户可用)';


--
-- Name: COLUMN platform_menu.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN platform_menu.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.description IS '备注';


--
-- Name: COLUMN platform_menu.parent_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.parent_id IS '父菜单ID';


--
-- Name: COLUMN platform_menu.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.id IS '主键ID';


--
-- Name: COLUMN platform_menu.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_menu.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_menu.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.created_time IS '创建时间';


--
-- Name: COLUMN platform_menu.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.updated_time IS '更新时间';


--
-- Name: COLUMN platform_menu.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_menu.deleted_time IS '删除时间';


--
-- Name: platform_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_menu_id_seq OWNER TO root;

--
-- Name: platform_menu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_menu_id_seq OWNED BY public.platform_menu.id;


--
-- Name: platform_order; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_order (
    order_no character varying(32) NOT NULL,
    package_id integer,
    plugin_id integer,
    order_type character varying(20) NOT NULL,
    amount integer NOT NULL,
    period_count integer NOT NULL,
    pay_method character varying(20),
    pay_time timestamp without time zone,
    expire_time timestamp without time zone NOT NULL,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL
);


ALTER TABLE public.platform_order OWNER TO root;

--
-- Name: TABLE platform_order; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_order IS '订单表';


--
-- Name: COLUMN platform_order.order_no; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.order_no IS '订单号';


--
-- Name: COLUMN platform_order.package_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.package_id IS '购买套餐(插件订单为空)';


--
-- Name: COLUMN platform_order.plugin_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.plugin_id IS '购买插件(套餐订单为空)';


--
-- Name: COLUMN platform_order.order_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.order_type IS 'new/renew/upgrade/downgrade/plugin';


--
-- Name: COLUMN platform_order.amount; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.amount IS '金额(分)';


--
-- Name: COLUMN platform_order.period_count; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.period_count IS '购买周期数';


--
-- Name: COLUMN platform_order.pay_method; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.pay_method IS 'alipay/wxpay';


--
-- Name: COLUMN platform_order.pay_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.pay_time IS '支付时间';


--
-- Name: COLUMN platform_order.expire_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.expire_time IS '订单过期时间(15分钟)';


--
-- Name: COLUMN platform_order.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.status IS '状态(0:待支付 1:已支付 2:已取消 3:已退款)';


--
-- Name: COLUMN platform_order.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.description IS '备注';


--
-- Name: COLUMN platform_order.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.id IS '主键ID';


--
-- Name: COLUMN platform_order.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_order.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_order.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.created_time IS '创建时间';


--
-- Name: COLUMN platform_order.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.updated_time IS '更新时间';


--
-- Name: COLUMN platform_order.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.deleted_time IS '删除时间';


--
-- Name: COLUMN platform_order.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_order.tenant_id IS '租户ID';


--
-- Name: platform_order_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_order_id_seq OWNER TO root;

--
-- Name: platform_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_order_id_seq OWNED BY public.platform_order.id;


--
-- Name: platform_package; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_package (
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    sort integer NOT NULL,
    price integer NOT NULL,
    period character varying(10) NOT NULL,
    trial_days integer NOT NULL,
    max_users integer NOT NULL,
    max_roles integer NOT NULL,
    max_depts integer NOT NULL,
    max_storage_mb integer NOT NULL,
    rate_limit integer NOT NULL,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone
);


ALTER TABLE public.platform_package OWNER TO root;

--
-- Name: TABLE platform_package; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_package IS '租户套餐表';


--
-- Name: COLUMN platform_package.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.name IS '套餐名称';


--
-- Name: COLUMN platform_package.code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.code IS '套餐编码';


--
-- Name: COLUMN platform_package.sort; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.sort IS '排序';


--
-- Name: COLUMN platform_package.price; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.price IS '价格(分)';


--
-- Name: COLUMN platform_package.period; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.period IS '计费周期(month/year)';


--
-- Name: COLUMN platform_package.trial_days; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.trial_days IS '免费试用天数';


--
-- Name: COLUMN platform_package.max_users; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.max_users IS '最大用户数';


--
-- Name: COLUMN platform_package.max_roles; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.max_roles IS '最大角色数';


--
-- Name: COLUMN platform_package.max_depts; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.max_depts IS '最大部门数';


--
-- Name: COLUMN platform_package.max_storage_mb; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.max_storage_mb IS '最大存储(MB)';


--
-- Name: COLUMN platform_package.rate_limit; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.rate_limit IS 'API速率限制(请求/10秒)';


--
-- Name: COLUMN platform_package.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN platform_package.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.description IS '备注';


--
-- Name: COLUMN platform_package.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.id IS '主键ID';


--
-- Name: COLUMN platform_package.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_package.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_package.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.created_time IS '创建时间';


--
-- Name: COLUMN platform_package.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.updated_time IS '更新时间';


--
-- Name: COLUMN platform_package.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package.deleted_time IS '删除时间';


--
-- Name: platform_package_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_package_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_package_id_seq OWNER TO root;

--
-- Name: platform_package_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_package_id_seq OWNED BY public.platform_package.id;


--
-- Name: platform_package_menu; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_package_menu (
    id integer NOT NULL,
    package_id integer NOT NULL,
    menu_id integer NOT NULL
);


ALTER TABLE public.platform_package_menu OWNER TO root;

--
-- Name: TABLE platform_package_menu; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_package_menu IS '套餐菜单关联表';


--
-- Name: COLUMN platform_package_menu.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package_menu.id IS '主键ID';


--
-- Name: COLUMN platform_package_menu.package_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package_menu.package_id IS '套餐ID';


--
-- Name: COLUMN platform_package_menu.menu_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package_menu.menu_id IS '菜单ID';


--
-- Name: platform_package_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_package_menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_package_menu_id_seq OWNER TO root;

--
-- Name: platform_package_menu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_package_menu_id_seq OWNED BY public.platform_package_menu.id;


--
-- Name: platform_package_plugin; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_package_plugin (
    id integer NOT NULL,
    package_id integer NOT NULL,
    plugin_id integer NOT NULL
);


ALTER TABLE public.platform_package_plugin OWNER TO root;

--
-- Name: TABLE platform_package_plugin; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_package_plugin IS '套餐插件关联表';


--
-- Name: COLUMN platform_package_plugin.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package_plugin.id IS '主键ID';


--
-- Name: COLUMN platform_package_plugin.package_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package_plugin.package_id IS '套餐ID';


--
-- Name: COLUMN platform_package_plugin.plugin_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_package_plugin.plugin_id IS '插件ID';


--
-- Name: platform_package_plugin_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_package_plugin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_package_plugin_id_seq OWNER TO root;

--
-- Name: platform_package_plugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_package_plugin_id_seq OWNED BY public.platform_package_plugin.id;


--
-- Name: platform_payment_record; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_payment_record (
    order_id integer NOT NULL,
    transaction_id character varying(64),
    pay_method character varying(20) NOT NULL,
    amount integer NOT NULL,
    raw_response text,
    pay_time timestamp without time zone,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL
);


ALTER TABLE public.platform_payment_record OWNER TO root;

--
-- Name: TABLE platform_payment_record; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_payment_record IS '支付记录表';


--
-- Name: COLUMN platform_payment_record.order_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.order_id IS '关联订单';


--
-- Name: COLUMN platform_payment_record.transaction_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.transaction_id IS '第三方交易号';


--
-- Name: COLUMN platform_payment_record.pay_method; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.pay_method IS '支付方式';


--
-- Name: COLUMN platform_payment_record.amount; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.amount IS '支付金额(分)';


--
-- Name: COLUMN platform_payment_record.raw_response; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.raw_response IS '原始回调JSON';


--
-- Name: COLUMN platform_payment_record.pay_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.pay_time IS '支付完成时间';


--
-- Name: COLUMN platform_payment_record.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.status IS '状态(0:处理中 1:成功 2:失败)';


--
-- Name: COLUMN platform_payment_record.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.description IS '备注';


--
-- Name: COLUMN platform_payment_record.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.id IS '主键ID';


--
-- Name: COLUMN platform_payment_record.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_payment_record.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_payment_record.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.created_time IS '创建时间';


--
-- Name: COLUMN platform_payment_record.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.updated_time IS '更新时间';


--
-- Name: COLUMN platform_payment_record.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.deleted_time IS '删除时间';


--
-- Name: COLUMN platform_payment_record.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_payment_record.tenant_id IS '租户ID';


--
-- Name: platform_payment_record_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_payment_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_payment_record_id_seq OWNER TO root;

--
-- Name: platform_payment_record_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_payment_record_id_seq OWNED BY public.platform_payment_record.id;


--
-- Name: platform_plugin; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_plugin (
    name character varying(100) NOT NULL,
    code character varying(50) NOT NULL,
    version character varying(20) NOT NULL,
    author character varying(100),
    icon character varying(500),
    category character varying(20) NOT NULL,
    price integer NOT NULL,
    menu_path character varying(200),
    permission_prefix character varying(100),
    dependencies text,
    sort integer NOT NULL,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone
);


ALTER TABLE public.platform_plugin OWNER TO root;

--
-- Name: TABLE platform_plugin; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_plugin IS '插件注册表';


--
-- Name: COLUMN platform_plugin.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.name IS '插件名称';


--
-- Name: COLUMN platform_plugin.code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.code IS '插件编码(module_xxx)';


--
-- Name: COLUMN platform_plugin.version; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.version IS '版本号';


--
-- Name: COLUMN platform_plugin.author; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.author IS '作者';


--
-- Name: COLUMN platform_plugin.icon; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.icon IS '图标URL';


--
-- Name: COLUMN platform_plugin.category; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.category IS '分类(tool/ai/monitor/business)';


--
-- Name: COLUMN platform_plugin.price; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.price IS '价格(分,0=免费)';


--
-- Name: COLUMN platform_plugin.menu_path; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.menu_path IS '菜单路径(安装后显示)';


--
-- Name: COLUMN platform_plugin.permission_prefix; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.permission_prefix IS '权限前缀';


--
-- Name: COLUMN platform_plugin.dependencies; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.dependencies IS '依赖插件编码(JSON数组)';


--
-- Name: COLUMN platform_plugin.sort; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.sort IS '排序';


--
-- Name: COLUMN platform_plugin.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN platform_plugin.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.description IS '备注';


--
-- Name: COLUMN platform_plugin.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.id IS '主键ID';


--
-- Name: COLUMN platform_plugin.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_plugin.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_plugin.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.created_time IS '创建时间';


--
-- Name: COLUMN platform_plugin.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.updated_time IS '更新时间';


--
-- Name: COLUMN platform_plugin.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_plugin.deleted_time IS '删除时间';


--
-- Name: platform_plugin_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_plugin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_plugin_id_seq OWNER TO root;

--
-- Name: platform_plugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_plugin_id_seq OWNED BY public.platform_plugin.id;


--
-- Name: platform_refund; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_refund (
    order_id integer NOT NULL,
    refund_no character varying(32) NOT NULL,
    amount integer NOT NULL,
    reason text NOT NULL,
    refund_transaction_id character varying(64),
    reviewer_id integer,
    review_time timestamp without time zone,
    reject_reason text,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL
);


ALTER TABLE public.platform_refund OWNER TO root;

--
-- Name: TABLE platform_refund; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_refund IS '退款表';


--
-- Name: COLUMN platform_refund.order_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.order_id IS '关联订单';


--
-- Name: COLUMN platform_refund.refund_no; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.refund_no IS '退款单号';


--
-- Name: COLUMN platform_refund.amount; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.amount IS '退款金额(分)';


--
-- Name: COLUMN platform_refund.reason; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.reason IS '退款原因';


--
-- Name: COLUMN platform_refund.refund_transaction_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.refund_transaction_id IS '退款交易号';


--
-- Name: COLUMN platform_refund.reviewer_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.reviewer_id IS '审核人';


--
-- Name: COLUMN platform_refund.review_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.review_time IS '审核时间';


--
-- Name: COLUMN platform_refund.reject_reason; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.reject_reason IS '驳回原因';


--
-- Name: COLUMN platform_refund.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.status IS '状态(1:申请中 2:已退款 3:已驳回 4:已取消)';


--
-- Name: COLUMN platform_refund.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.description IS '备注';


--
-- Name: COLUMN platform_refund.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.id IS '主键ID';


--
-- Name: COLUMN platform_refund.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_refund.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_refund.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.created_time IS '创建时间';


--
-- Name: COLUMN platform_refund.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.updated_time IS '更新时间';


--
-- Name: COLUMN platform_refund.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.deleted_time IS '删除时间';


--
-- Name: COLUMN platform_refund.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_refund.tenant_id IS '租户ID';


--
-- Name: platform_refund_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_refund_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_refund_id_seq OWNER TO root;

--
-- Name: platform_refund_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_refund_id_seq OWNED BY public.platform_refund.id;


--
-- Name: platform_tenant; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_tenant (
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    contact_name character varying(64),
    contact_phone character varying(20),
    contact_email character varying(128),
    address character varying(255),
    domain character varying(255),
    logo_url character varying(500),
    sort integer NOT NULL,
    package_id integer,
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    version character varying(20),
    favicon character varying(500),
    login_bg character varying(500),
    copyright character varying(255),
    keep_record character varying(100),
    help_doc character varying(500),
    privacy character varying(500),
    clause character varying(500),
    git_code character varying(500),
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone
);


ALTER TABLE public.platform_tenant OWNER TO root;

--
-- Name: TABLE platform_tenant; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_tenant IS '租户表';


--
-- Name: COLUMN platform_tenant.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.name IS '租户名称';


--
-- Name: COLUMN platform_tenant.code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.code IS '租户编码';


--
-- Name: COLUMN platform_tenant.contact_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.contact_name IS '联系人姓名';


--
-- Name: COLUMN platform_tenant.contact_phone; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.contact_phone IS '联系人电话';


--
-- Name: COLUMN platform_tenant.contact_email; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.contact_email IS '联系人邮箱';


--
-- Name: COLUMN platform_tenant.address; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.address IS '地址';


--
-- Name: COLUMN platform_tenant.domain; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.domain IS '域名';


--
-- Name: COLUMN platform_tenant.logo_url; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.logo_url IS 'Logo URL';


--
-- Name: COLUMN platform_tenant.sort; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.sort IS '排序';


--
-- Name: COLUMN platform_tenant.package_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.package_id IS '关联套餐ID';


--
-- Name: COLUMN platform_tenant.start_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.start_time IS '开始时间';


--
-- Name: COLUMN platform_tenant.end_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.end_time IS '结束时间';


--
-- Name: COLUMN platform_tenant.version; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.version IS '版本号';


--
-- Name: COLUMN platform_tenant.favicon; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.favicon IS 'favicon地址';


--
-- Name: COLUMN platform_tenant.login_bg; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.login_bg IS '登录背景地址';


--
-- Name: COLUMN platform_tenant.copyright; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.copyright IS '版权信息';


--
-- Name: COLUMN platform_tenant.keep_record; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.keep_record IS '备案号';


--
-- Name: COLUMN platform_tenant.help_doc; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.help_doc IS '帮助文档地址';


--
-- Name: COLUMN platform_tenant.privacy; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.privacy IS '隐私政策地址';


--
-- Name: COLUMN platform_tenant.clause; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.clause IS '服务条款地址';


--
-- Name: COLUMN platform_tenant.git_code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.git_code IS '源码地址';


--
-- Name: COLUMN platform_tenant.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN platform_tenant.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.description IS '备注';


--
-- Name: COLUMN platform_tenant.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.id IS '主键ID';


--
-- Name: COLUMN platform_tenant.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN platform_tenant.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN platform_tenant.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.created_time IS '创建时间';


--
-- Name: COLUMN platform_tenant.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.updated_time IS '更新时间';


--
-- Name: COLUMN platform_tenant.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant.deleted_time IS '删除时间';


--
-- Name: platform_tenant_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_tenant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_tenant_id_seq OWNER TO root;

--
-- Name: platform_tenant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_tenant_id_seq OWNED BY public.platform_tenant.id;


--
-- Name: platform_tenant_plugin; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_tenant_plugin (
    id integer NOT NULL,
    tenant_id integer NOT NULL,
    plugin_id integer NOT NULL,
    enabled boolean NOT NULL,
    purchased boolean NOT NULL,
    installed_time timestamp without time zone NOT NULL
);


ALTER TABLE public.platform_tenant_plugin OWNER TO root;

--
-- Name: TABLE platform_tenant_plugin; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_tenant_plugin IS '租户插件关联表';


--
-- Name: COLUMN platform_tenant_plugin.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant_plugin.id IS '主键ID';


--
-- Name: COLUMN platform_tenant_plugin.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant_plugin.tenant_id IS '租户ID';


--
-- Name: COLUMN platform_tenant_plugin.plugin_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant_plugin.plugin_id IS '插件ID';


--
-- Name: COLUMN platform_tenant_plugin.enabled; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant_plugin.enabled IS '启用(True:启用 False:禁用)';


--
-- Name: COLUMN platform_tenant_plugin.purchased; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant_plugin.purchased IS '是否已购买(True:已购买 False:未购买)';


--
-- Name: COLUMN platform_tenant_plugin.installed_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_tenant_plugin.installed_time IS '安装时间';


--
-- Name: platform_tenant_plugin_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_tenant_plugin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_tenant_plugin_id_seq OWNER TO root;

--
-- Name: platform_tenant_plugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_tenant_plugin_id_seq OWNED BY public.platform_tenant_plugin.id;


--
-- Name: platform_user_tenant; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.platform_user_tenant (
    id integer NOT NULL,
    user_id integer NOT NULL,
    tenant_id integer NOT NULL,
    role character varying(20) NOT NULL,
    is_default smallint NOT NULL,
    create_time timestamp without time zone NOT NULL
);


ALTER TABLE public.platform_user_tenant OWNER TO root;

--
-- Name: TABLE platform_user_tenant; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.platform_user_tenant IS '用户租户关联表';


--
-- Name: COLUMN platform_user_tenant.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_user_tenant.id IS '主键ID';


--
-- Name: COLUMN platform_user_tenant.user_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_user_tenant.user_id IS '用户ID';


--
-- Name: COLUMN platform_user_tenant.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_user_tenant.tenant_id IS '租户ID';


--
-- Name: COLUMN platform_user_tenant.role; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_user_tenant.role IS '租户内角色(owner:拥有者 admin:管理员 member:成员)';


--
-- Name: COLUMN platform_user_tenant.is_default; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_user_tenant.is_default IS '是否默认租户(0:否 1:是)';


--
-- Name: COLUMN platform_user_tenant.create_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.platform_user_tenant.create_time IS '创建时间';


--
-- Name: platform_user_tenant_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.platform_user_tenant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platform_user_tenant_id_seq OWNER TO root;

--
-- Name: platform_user_tenant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.platform_user_tenant_id_seq OWNED BY public.platform_user_tenant.id;


--
-- Name: sys_dept; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_dept (
    name character varying(64) NOT NULL,
    status integer NOT NULL,
    description text,
    "order" integer NOT NULL,
    code character varying(64) NOT NULL,
    leader character varying(32),
    phone character varying(20),
    email character varying(128),
    parent_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.sys_dept OWNER TO root;

--
-- Name: TABLE sys_dept; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_dept IS '部门表';


--
-- Name: COLUMN sys_dept.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.name IS '部门名称';


--
-- Name: COLUMN sys_dept.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN sys_dept.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.description IS '备注';


--
-- Name: COLUMN sys_dept."order"; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept."order" IS '显示排序';


--
-- Name: COLUMN sys_dept.code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.code IS '部门编码';


--
-- Name: COLUMN sys_dept.leader; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.leader IS '部门负责人';


--
-- Name: COLUMN sys_dept.phone; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.phone IS '手机';


--
-- Name: COLUMN sys_dept.email; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.email IS '邮箱';


--
-- Name: COLUMN sys_dept.parent_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.parent_id IS '父级部门ID';


--
-- Name: COLUMN sys_dept.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.id IS '主键ID';


--
-- Name: COLUMN sys_dept.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_dept.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_dept.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.created_time IS '创建时间';


--
-- Name: COLUMN sys_dept.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.updated_time IS '更新时间';


--
-- Name: COLUMN sys_dept.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_dept.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.tenant_id IS '租户ID';


--
-- Name: COLUMN sys_dept.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.created_id IS '创建人ID';


--
-- Name: COLUMN sys_dept.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.updated_id IS '更新人ID';


--
-- Name: COLUMN sys_dept.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.deleted_id IS '删除人ID';


--
-- Name: sys_dept_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_dept_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_dept_id_seq OWNER TO root;

--
-- Name: sys_dept_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_dept_id_seq OWNED BY public.sys_dept.id;


--
-- Name: sys_dict_data; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_dict_data (
    status integer NOT NULL,
    description text,
    dict_sort integer NOT NULL,
    dict_label character varying(255) NOT NULL,
    dict_value character varying(255) NOT NULL,
    css_class character varying(255),
    list_class character varying(255),
    is_default boolean NOT NULL,
    dict_type character varying(255) NOT NULL,
    dict_type_id integer NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL
);


ALTER TABLE public.sys_dict_data OWNER TO root;

--
-- Name: TABLE sys_dict_data; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_dict_data IS '字典数据表';


--
-- Name: COLUMN sys_dict_data.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN sys_dict_data.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.description IS '备注';


--
-- Name: COLUMN sys_dict_data.dict_sort; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.dict_sort IS '字典排序';


--
-- Name: COLUMN sys_dict_data.dict_label; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.dict_label IS '字典标签';


--
-- Name: COLUMN sys_dict_data.dict_value; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.dict_value IS '字典键值';


--
-- Name: COLUMN sys_dict_data.css_class; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.css_class IS '样式属性（其他样式扩展）';


--
-- Name: COLUMN sys_dict_data.list_class; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.list_class IS '表格回显样式';


--
-- Name: COLUMN sys_dict_data.is_default; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.is_default IS '是否默认(True是 False否)';


--
-- Name: COLUMN sys_dict_data.dict_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.dict_type IS '字典类型';


--
-- Name: COLUMN sys_dict_data.dict_type_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.dict_type_id IS '字典类型ID';


--
-- Name: COLUMN sys_dict_data.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.id IS '主键ID';


--
-- Name: COLUMN sys_dict_data.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_dict_data.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_dict_data.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.created_time IS '创建时间';


--
-- Name: COLUMN sys_dict_data.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.updated_time IS '更新时间';


--
-- Name: COLUMN sys_dict_data.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_dict_data.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.tenant_id IS '租户ID';


--
-- Name: sys_dict_data_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_dict_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_dict_data_id_seq OWNER TO root;

--
-- Name: sys_dict_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_dict_data_id_seq OWNED BY public.sys_dict_data.id;


--
-- Name: sys_dict_type; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_dict_type (
    dict_name character varying(64) NOT NULL,
    dict_type character varying(255) NOT NULL,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL
);


ALTER TABLE public.sys_dict_type OWNER TO root;

--
-- Name: TABLE sys_dict_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_dict_type IS '字典类型表';


--
-- Name: COLUMN sys_dict_type.dict_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.dict_name IS '字典名称';


--
-- Name: COLUMN sys_dict_type.dict_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.dict_type IS '字典类型';


--
-- Name: COLUMN sys_dict_type.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN sys_dict_type.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.description IS '备注';


--
-- Name: COLUMN sys_dict_type.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.id IS '主键ID';


--
-- Name: COLUMN sys_dict_type.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_dict_type.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_dict_type.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.created_time IS '创建时间';


--
-- Name: COLUMN sys_dict_type.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.updated_time IS '更新时间';


--
-- Name: COLUMN sys_dict_type.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_dict_type.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.tenant_id IS '租户ID';


--
-- Name: sys_dict_type_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_dict_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_dict_type_id_seq OWNER TO root;

--
-- Name: sys_dict_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_dict_type_id_seq OWNED BY public.sys_dict_type.id;


--
-- Name: sys_login_log; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_login_log (
    status integer NOT NULL,
    description text,
    username character varying(64) NOT NULL,
    login_location character varying(255),
    login_ip character varying(50),
    request_os character varying(64),
    request_browser character varying(64),
    msg character varying(255),
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.sys_login_log OWNER TO root;

--
-- Name: TABLE sys_login_log; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_login_log IS '登录日志表';


--
-- Name: COLUMN sys_login_log.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.status IS '登录状态(1成功 2失败)';


--
-- Name: COLUMN sys_login_log.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.description IS '备注';


--
-- Name: COLUMN sys_login_log.username; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.username IS '用户名';


--
-- Name: COLUMN sys_login_log.login_location; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.login_location IS '登录位置';


--
-- Name: COLUMN sys_login_log.login_ip; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.login_ip IS '登录IP地址';


--
-- Name: COLUMN sys_login_log.request_os; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.request_os IS '操作系统';


--
-- Name: COLUMN sys_login_log.request_browser; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.request_browser IS '浏览器';


--
-- Name: COLUMN sys_login_log.msg; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.msg IS '提示消息';


--
-- Name: COLUMN sys_login_log.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.id IS '主键ID';


--
-- Name: COLUMN sys_login_log.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_login_log.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_login_log.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.created_time IS '创建时间';


--
-- Name: COLUMN sys_login_log.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.updated_time IS '更新时间';


--
-- Name: COLUMN sys_login_log.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_login_log.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.tenant_id IS '租户ID';


--
-- Name: COLUMN sys_login_log.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.created_id IS '创建人ID';


--
-- Name: COLUMN sys_login_log.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.updated_id IS '更新人ID';


--
-- Name: COLUMN sys_login_log.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_login_log.deleted_id IS '删除人ID';


--
-- Name: sys_login_log_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_login_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_login_log_id_seq OWNER TO root;

--
-- Name: sys_login_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_login_log_id_seq OWNED BY public.sys_login_log.id;


--
-- Name: sys_notice; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_notice (
    notice_title character varying(64) NOT NULL,
    notice_type character varying(1) NOT NULL,
    notice_content text,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.sys_notice OWNER TO root;

--
-- Name: TABLE sys_notice; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_notice IS '通知公告表';


--
-- Name: COLUMN sys_notice.notice_title; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.notice_title IS '公告标题';


--
-- Name: COLUMN sys_notice.notice_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.notice_type IS '公告类型(1通知 2公告)';


--
-- Name: COLUMN sys_notice.notice_content; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.notice_content IS '公告内容';


--
-- Name: COLUMN sys_notice.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN sys_notice.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.description IS '备注';


--
-- Name: COLUMN sys_notice.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.id IS '主键ID';


--
-- Name: COLUMN sys_notice.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_notice.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_notice.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.created_time IS '创建时间';


--
-- Name: COLUMN sys_notice.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.updated_time IS '更新时间';


--
-- Name: COLUMN sys_notice.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_notice.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.tenant_id IS '租户ID';


--
-- Name: COLUMN sys_notice.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.created_id IS '创建人ID';


--
-- Name: COLUMN sys_notice.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.updated_id IS '更新人ID';


--
-- Name: COLUMN sys_notice.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.deleted_id IS '删除人ID';


--
-- Name: sys_notice_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_notice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_notice_id_seq OWNER TO root;

--
-- Name: sys_notice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_notice_id_seq OWNED BY public.sys_notice.id;


--
-- Name: sys_notice_read; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_notice_read (
    user_id integer NOT NULL,
    notice_id integer NOT NULL,
    read_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_notice_read OWNER TO root;

--
-- Name: TABLE sys_notice_read; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_notice_read IS '通知已读记录表';


--
-- Name: COLUMN sys_notice_read.user_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice_read.user_id IS '用户ID';


--
-- Name: COLUMN sys_notice_read.notice_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice_read.notice_id IS '通知ID';


--
-- Name: COLUMN sys_notice_read.read_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice_read.read_time IS '已读时间';


--
-- Name: sys_operation_log; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_operation_log (
    status integer NOT NULL,
    description text,
    request_path character varying(255) NOT NULL,
    request_method character varying(10) NOT NULL,
    request_payload text,
    response_code integer NOT NULL,
    response_json text,
    process_time character varying(20),
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.sys_operation_log OWNER TO root;

--
-- Name: TABLE sys_operation_log; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_operation_log IS '操作日志表';


--
-- Name: COLUMN sys_operation_log.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN sys_operation_log.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.description IS '备注';


--
-- Name: COLUMN sys_operation_log.request_path; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.request_path IS '请求路径';


--
-- Name: COLUMN sys_operation_log.request_method; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.request_method IS '请求方式';


--
-- Name: COLUMN sys_operation_log.request_payload; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.request_payload IS '请求体';


--
-- Name: COLUMN sys_operation_log.response_code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.response_code IS '响应状态码';


--
-- Name: COLUMN sys_operation_log.response_json; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.response_json IS '响应体';


--
-- Name: COLUMN sys_operation_log.process_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.process_time IS '处理时间';


--
-- Name: COLUMN sys_operation_log.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.id IS '主键ID';


--
-- Name: COLUMN sys_operation_log.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_operation_log.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_operation_log.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.created_time IS '创建时间';


--
-- Name: COLUMN sys_operation_log.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.updated_time IS '更新时间';


--
-- Name: COLUMN sys_operation_log.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_operation_log.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.tenant_id IS '租户ID';


--
-- Name: COLUMN sys_operation_log.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.created_id IS '创建人ID';


--
-- Name: COLUMN sys_operation_log.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.updated_id IS '更新人ID';


--
-- Name: COLUMN sys_operation_log.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_operation_log.deleted_id IS '删除人ID';


--
-- Name: sys_operation_log_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_operation_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_operation_log_id_seq OWNER TO root;

--
-- Name: sys_operation_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_operation_log_id_seq OWNED BY public.sys_operation_log.id;


--
-- Name: sys_param; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_param (
    config_name character varying(64) NOT NULL,
    config_key character varying(500) NOT NULL,
    config_value character varying(500),
    config_type boolean,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.sys_param OWNER TO root;

--
-- Name: TABLE sys_param; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_param IS '系统参数表';


--
-- Name: COLUMN sys_param.config_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.config_name IS '参数名称';


--
-- Name: COLUMN sys_param.config_key; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.config_key IS '参数键名';


--
-- Name: COLUMN sys_param.config_value; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.config_value IS '参数键值';


--
-- Name: COLUMN sys_param.config_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.config_type IS '系统内置(True:是 False:否)';


--
-- Name: COLUMN sys_param.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN sys_param.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.description IS '备注';


--
-- Name: COLUMN sys_param.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.id IS '主键ID';


--
-- Name: COLUMN sys_param.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_param.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_param.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.created_time IS '创建时间';


--
-- Name: COLUMN sys_param.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.updated_time IS '更新时间';


--
-- Name: COLUMN sys_param.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_param.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.tenant_id IS '租户ID';


--
-- Name: COLUMN sys_param.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.created_id IS '创建人ID';


--
-- Name: COLUMN sys_param.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.updated_id IS '更新人ID';


--
-- Name: COLUMN sys_param.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.deleted_id IS '删除人ID';


--
-- Name: sys_param_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_param_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_param_id_seq OWNER TO root;

--
-- Name: sys_param_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_param_id_seq OWNED BY public.sys_param.id;


--
-- Name: sys_position; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_position (
    name character varying(64) NOT NULL,
    code character varying(64) NOT NULL,
    "order" integer NOT NULL,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.sys_position OWNER TO root;

--
-- Name: TABLE sys_position; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_position IS '岗位表';


--
-- Name: COLUMN sys_position.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.name IS '岗位名称';


--
-- Name: COLUMN sys_position.code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.code IS '岗位编码';


--
-- Name: COLUMN sys_position."order"; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position."order" IS '显示排序';


--
-- Name: COLUMN sys_position.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN sys_position.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.description IS '备注';


--
-- Name: COLUMN sys_position.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.id IS '主键ID';


--
-- Name: COLUMN sys_position.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_position.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_position.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.created_time IS '创建时间';


--
-- Name: COLUMN sys_position.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.updated_time IS '更新时间';


--
-- Name: COLUMN sys_position.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_position.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.tenant_id IS '租户ID';


--
-- Name: COLUMN sys_position.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.created_id IS '创建人ID';


--
-- Name: COLUMN sys_position.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.updated_id IS '更新人ID';


--
-- Name: COLUMN sys_position.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.deleted_id IS '删除人ID';


--
-- Name: sys_position_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_position_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_position_id_seq OWNER TO root;

--
-- Name: sys_position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_position_id_seq OWNED BY public.sys_position.id;


--
-- Name: sys_role; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_role (
    name character varying(64) NOT NULL,
    code character varying(64) NOT NULL,
    "order" integer NOT NULL,
    status integer NOT NULL,
    description text,
    data_scope integer NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.sys_role OWNER TO root;

--
-- Name: TABLE sys_role; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_role IS '角色表';


--
-- Name: COLUMN sys_role.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.name IS '角色名称';


--
-- Name: COLUMN sys_role.code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.code IS '角色编码';


--
-- Name: COLUMN sys_role."order"; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role."order" IS '显示排序';


--
-- Name: COLUMN sys_role.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN sys_role.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.description IS '备注';


--
-- Name: COLUMN sys_role.data_scope; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.data_scope IS '数据权限范围(1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义)';


--
-- Name: COLUMN sys_role.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.id IS '主键ID';


--
-- Name: COLUMN sys_role.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_role.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_role.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.created_time IS '创建时间';


--
-- Name: COLUMN sys_role.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.updated_time IS '更新时间';


--
-- Name: COLUMN sys_role.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_role.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.tenant_id IS '租户ID';


--
-- Name: COLUMN sys_role.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.created_id IS '创建人ID';


--
-- Name: COLUMN sys_role.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.updated_id IS '更新人ID';


--
-- Name: COLUMN sys_role.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.deleted_id IS '删除人ID';


--
-- Name: sys_role_depts; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_role_depts (
    role_id integer NOT NULL,
    dept_id integer NOT NULL
);


ALTER TABLE public.sys_role_depts OWNER TO root;

--
-- Name: TABLE sys_role_depts; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_role_depts IS '角色部门关联表';


--
-- Name: COLUMN sys_role_depts.role_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role_depts.role_id IS '角色ID';


--
-- Name: COLUMN sys_role_depts.dept_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role_depts.dept_id IS '部门ID';


--
-- Name: sys_role_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_role_id_seq OWNER TO root;

--
-- Name: sys_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_role_id_seq OWNED BY public.sys_role.id;


--
-- Name: sys_role_menus; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_role_menus (
    role_id integer NOT NULL,
    menu_id integer NOT NULL
);


ALTER TABLE public.sys_role_menus OWNER TO root;

--
-- Name: TABLE sys_role_menus; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_role_menus IS '角色菜单关联表';


--
-- Name: COLUMN sys_role_menus.role_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role_menus.role_id IS '角色ID';


--
-- Name: COLUMN sys_role_menus.menu_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role_menus.menu_id IS '菜单ID';


--
-- Name: sys_ticket; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_ticket (
    title character varying(200) NOT NULL,
    status integer NOT NULL,
    description text,
    ticket_content text,
    summary text,
    ticket_type character varying(20) NOT NULL,
    images text,
    reply text,
    assigned_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.sys_ticket OWNER TO root;

--
-- Name: TABLE sys_ticket; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_ticket IS '工单表';


--
-- Name: COLUMN sys_ticket.title; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.title IS '工单标题';


--
-- Name: COLUMN sys_ticket.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.status IS '状态(0:待处理 1:处理中 2:已完成 3:已关闭)';


--
-- Name: COLUMN sys_ticket.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.description IS '备注';


--
-- Name: COLUMN sys_ticket.ticket_content; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.ticket_content IS '工单内容（富文本）';


--
-- Name: COLUMN sys_ticket.summary; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.summary IS '工单内容（纯文本摘要）';


--
-- Name: COLUMN sys_ticket.ticket_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.ticket_type IS '工单类型(suggestion:建议 bug:缺陷 optimize:优化 other:其他)';


--
-- Name: COLUMN sys_ticket.images; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.images IS '图片URL列表(JSON数组)';


--
-- Name: COLUMN sys_ticket.reply; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.reply IS '回复内容';


--
-- Name: COLUMN sys_ticket.assigned_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.assigned_id IS '处理人ID';


--
-- Name: COLUMN sys_ticket.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.id IS '主键ID';


--
-- Name: COLUMN sys_ticket.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_ticket.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_ticket.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.created_time IS '创建时间';


--
-- Name: COLUMN sys_ticket.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.updated_time IS '更新时间';


--
-- Name: COLUMN sys_ticket.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_ticket.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.tenant_id IS '租户ID';


--
-- Name: COLUMN sys_ticket.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.created_id IS '创建人ID';


--
-- Name: COLUMN sys_ticket.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.updated_id IS '更新人ID';


--
-- Name: COLUMN sys_ticket.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_ticket.deleted_id IS '删除人ID';


--
-- Name: sys_ticket_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_ticket_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_ticket_id_seq OWNER TO root;

--
-- Name: sys_ticket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_ticket_id_seq OWNED BY public.sys_ticket.id;


--
-- Name: sys_user; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_user (
    username character varying(64) NOT NULL,
    password character varying(255) NOT NULL,
    name character varying(32) NOT NULL,
    mobile character varying(11),
    email character varying(64),
    gender character varying(1),
    avatar character varying(255),
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone,
    gitee_login character varying(32),
    github_login character varying(32),
    wx_login character varying(32),
    qq_login character varying(32),
    status integer NOT NULL,
    description text,
    dept_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.sys_user OWNER TO root;

--
-- Name: TABLE sys_user; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_user IS '用户表';


--
-- Name: COLUMN sys_user.username; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.username IS '用户名/登录账号';


--
-- Name: COLUMN sys_user.password; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.password IS '密码哈希';


--
-- Name: COLUMN sys_user.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.name IS '昵称';


--
-- Name: COLUMN sys_user.mobile; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.mobile IS '手机号';


--
-- Name: COLUMN sys_user.email; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.email IS '邮箱';


--
-- Name: COLUMN sys_user.gender; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.gender IS '性别(0:男 1:女 2:未知)';


--
-- Name: COLUMN sys_user.avatar; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.avatar IS '头像URL地址';


--
-- Name: COLUMN sys_user.is_superuser; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.is_superuser IS '是否超管';


--
-- Name: COLUMN sys_user.last_login; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.last_login IS '最后登录时间';


--
-- Name: COLUMN sys_user.gitee_login; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.gitee_login IS 'Gitee登录';


--
-- Name: COLUMN sys_user.github_login; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.github_login IS 'Github登录';


--
-- Name: COLUMN sys_user.wx_login; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.wx_login IS '微信登录';


--
-- Name: COLUMN sys_user.qq_login; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.qq_login IS 'QQ登录';


--
-- Name: COLUMN sys_user.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN sys_user.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.description IS '备注';


--
-- Name: COLUMN sys_user.dept_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.dept_id IS '部门ID';


--
-- Name: COLUMN sys_user.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.id IS '主键ID';


--
-- Name: COLUMN sys_user.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_user.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN sys_user.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.created_time IS '创建时间';


--
-- Name: COLUMN sys_user.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.updated_time IS '更新时间';


--
-- Name: COLUMN sys_user.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.deleted_time IS '删除时间';


--
-- Name: COLUMN sys_user.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.tenant_id IS '租户ID';


--
-- Name: COLUMN sys_user.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.created_id IS '创建人ID';


--
-- Name: COLUMN sys_user.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.updated_id IS '更新人ID';


--
-- Name: COLUMN sys_user.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.deleted_id IS '删除人ID';


--
-- Name: sys_user_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_user_id_seq OWNER TO root;

--
-- Name: sys_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_user_id_seq OWNED BY public.sys_user.id;


--
-- Name: sys_user_positions; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_user_positions (
    user_id integer NOT NULL,
    position_id integer NOT NULL
);


ALTER TABLE public.sys_user_positions OWNER TO root;

--
-- Name: TABLE sys_user_positions; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_user_positions IS '用户岗位关联表';


--
-- Name: COLUMN sys_user_positions.user_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user_positions.user_id IS '用户ID';


--
-- Name: COLUMN sys_user_positions.position_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user_positions.position_id IS '岗位ID';


--
-- Name: sys_user_roles; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_user_roles (
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.sys_user_roles OWNER TO root;

--
-- Name: TABLE sys_user_roles; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_user_roles IS '用户角色关联表';


--
-- Name: COLUMN sys_user_roles.user_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user_roles.user_id IS '用户ID';


--
-- Name: COLUMN sys_user_roles.role_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user_roles.role_id IS '角色ID';


--
-- Name: task_job; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.task_job (
    job_id character varying(64) NOT NULL,
    job_name character varying(128),
    trigger_type character varying(32),
    next_run_time character varying(64),
    job_state text,
    result text,
    error text,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL
);


ALTER TABLE public.task_job OWNER TO root;

--
-- Name: TABLE task_job; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.task_job IS '任务执行日志表';


--
-- Name: COLUMN task_job.job_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.job_id IS '任务ID';


--
-- Name: COLUMN task_job.job_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.job_name IS '任务名称';


--
-- Name: COLUMN task_job.trigger_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.trigger_type IS '触发方式: cron/interval/date/manual';


--
-- Name: COLUMN task_job.next_run_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.next_run_time IS '下次执行时间';


--
-- Name: COLUMN task_job.job_state; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.job_state IS '任务状态信息';


--
-- Name: COLUMN task_job.result; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.result IS '执行结果';


--
-- Name: COLUMN task_job.error; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.error IS '错误信息';


--
-- Name: COLUMN task_job.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.status IS '执行状态(0:待执行 1:执行中 2:成功 3:失败 4:超时 5:已取消)';


--
-- Name: COLUMN task_job.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.description IS '备注';


--
-- Name: COLUMN task_job.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.id IS '主键ID';


--
-- Name: COLUMN task_job.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_job.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN task_job.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.created_time IS '创建时间';


--
-- Name: COLUMN task_job.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.updated_time IS '更新时间';


--
-- Name: COLUMN task_job.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.deleted_time IS '删除时间';


--
-- Name: COLUMN task_job.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.tenant_id IS '租户ID';


--
-- Name: task_job_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.task_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_job_id_seq OWNER TO root;

--
-- Name: task_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.task_job_id_seq OWNED BY public.task_job.id;


--
-- Name: task_node; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.task_node (
    name character varying(64) NOT NULL,
    code character varying(32) NOT NULL,
    jobstore character varying(64),
    executor character varying(64),
    trigger character varying(64),
    trigger_args text,
    func text,
    args text,
    kwargs text,
    "coalesce" boolean,
    max_instances integer,
    start_date character varying(64),
    end_date character varying(64),
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.task_node OWNER TO root;

--
-- Name: TABLE task_node; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.task_node IS '节点类型表';


--
-- Name: COLUMN task_node.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.name IS '节点名称';


--
-- Name: COLUMN task_node.code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.code IS '节点编码';


--
-- Name: COLUMN task_node.jobstore; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.jobstore IS '存储器';


--
-- Name: COLUMN task_node.executor; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.executor IS '执行器';


--
-- Name: COLUMN task_node.trigger; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.trigger IS '触发器';


--
-- Name: COLUMN task_node.trigger_args; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.trigger_args IS '触发器参数';


--
-- Name: COLUMN task_node.func; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.func IS '代码块';


--
-- Name: COLUMN task_node.args; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.args IS '位置参数';


--
-- Name: COLUMN task_node.kwargs; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.kwargs IS '关键字参数';


--
-- Name: COLUMN task_node."coalesce"; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node."coalesce" IS '是否合并运行';


--
-- Name: COLUMN task_node.max_instances; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.max_instances IS '最大实例数';


--
-- Name: COLUMN task_node.start_date; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.start_date IS '开始时间';


--
-- Name: COLUMN task_node.end_date; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.end_date IS '结束时间';


--
-- Name: COLUMN task_node.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN task_node.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.description IS '备注';


--
-- Name: COLUMN task_node.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.id IS '主键ID';


--
-- Name: COLUMN task_node.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_node.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN task_node.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.created_time IS '创建时间';


--
-- Name: COLUMN task_node.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.updated_time IS '更新时间';


--
-- Name: COLUMN task_node.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.deleted_time IS '删除时间';


--
-- Name: COLUMN task_node.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.tenant_id IS '租户ID';


--
-- Name: COLUMN task_node.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.created_id IS '创建人ID';


--
-- Name: COLUMN task_node.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.updated_id IS '更新人ID';


--
-- Name: COLUMN task_node.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.deleted_id IS '删除人ID';


--
-- Name: task_node_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.task_node_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_node_id_seq OWNER TO root;

--
-- Name: task_node_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.task_node_id_seq OWNED BY public.task_node.id;


--
-- Name: task_workflow; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.task_workflow (
    name character varying(128) NOT NULL,
    code character varying(64) NOT NULL,
    nodes json,
    edges json,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.task_workflow OWNER TO root;

--
-- Name: TABLE task_workflow; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.task_workflow IS '工作流定义表';


--
-- Name: COLUMN task_workflow.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.name IS '流程名称';


--
-- Name: COLUMN task_workflow.code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.code IS '流程编码';


--
-- Name: COLUMN task_workflow.nodes; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.nodes IS 'VueFlow节点';


--
-- Name: COLUMN task_workflow.edges; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.edges IS 'VueFlow连接线';


--
-- Name: COLUMN task_workflow.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.status IS '状态(0:草稿 1:已发布 2:已归档)';


--
-- Name: COLUMN task_workflow.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.description IS '备注';


--
-- Name: COLUMN task_workflow.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.id IS '主键ID';


--
-- Name: COLUMN task_workflow.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_workflow.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN task_workflow.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.created_time IS '创建时间';


--
-- Name: COLUMN task_workflow.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.updated_time IS '更新时间';


--
-- Name: COLUMN task_workflow.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.deleted_time IS '删除时间';


--
-- Name: COLUMN task_workflow.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.tenant_id IS '租户ID';


--
-- Name: COLUMN task_workflow.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.created_id IS '创建人ID';


--
-- Name: COLUMN task_workflow.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.updated_id IS '更新人ID';


--
-- Name: COLUMN task_workflow.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.deleted_id IS '删除人ID';


--
-- Name: task_workflow_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.task_workflow_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_workflow_id_seq OWNER TO root;

--
-- Name: task_workflow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.task_workflow_id_seq OWNED BY public.task_workflow.id;


--
-- Name: task_workflow_node_type; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.task_workflow_node_type (
    name character varying(128) NOT NULL,
    code character varying(64) NOT NULL,
    category character varying(32) NOT NULL,
    func text NOT NULL,
    args text,
    kwargs text,
    sort_order integer NOT NULL,
    is_active boolean NOT NULL,
    status integer NOT NULL,
    description text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    deleted_time timestamp without time zone,
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer,
    deleted_id integer
);


ALTER TABLE public.task_workflow_node_type OWNER TO root;

--
-- Name: TABLE task_workflow_node_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.task_workflow_node_type IS '工作流编排节点类型（非定时任务节点）';


--
-- Name: COLUMN task_workflow_node_type.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.name IS '显示名称';


--
-- Name: COLUMN task_workflow_node_type.code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.code IS '节点编码，对应画布 node.type';


--
-- Name: COLUMN task_workflow_node_type.category; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.category IS '分类: trigger/action/condition/control';


--
-- Name: COLUMN task_workflow_node_type.func; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.func IS 'Python 代码块，须定义 handler(*args,**kwargs)';


--
-- Name: COLUMN task_workflow_node_type.args; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.args IS '默认位置参数，逗号分隔';


--
-- Name: COLUMN task_workflow_node_type.kwargs; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.kwargs IS '默认关键字参数 JSON';


--
-- Name: COLUMN task_workflow_node_type.sort_order; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.sort_order IS '排序';


--
-- Name: COLUMN task_workflow_node_type.is_active; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.is_active IS '是否启用';


--
-- Name: COLUMN task_workflow_node_type.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.status IS '状态(0:启动 1:停用)';


--
-- Name: COLUMN task_workflow_node_type.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.description IS '备注';


--
-- Name: COLUMN task_workflow_node_type.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.id IS '主键ID';


--
-- Name: COLUMN task_workflow_node_type.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_workflow_node_type.is_deleted; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.is_deleted IS '是否已删除(0:未删除 1:已删除)';


--
-- Name: COLUMN task_workflow_node_type.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.created_time IS '创建时间';


--
-- Name: COLUMN task_workflow_node_type.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.updated_time IS '更新时间';


--
-- Name: COLUMN task_workflow_node_type.deleted_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.deleted_time IS '删除时间';


--
-- Name: COLUMN task_workflow_node_type.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.tenant_id IS '租户ID';


--
-- Name: COLUMN task_workflow_node_type.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.created_id IS '创建人ID';


--
-- Name: COLUMN task_workflow_node_type.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.updated_id IS '更新人ID';


--
-- Name: COLUMN task_workflow_node_type.deleted_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.deleted_id IS '删除人ID';


--
-- Name: task_workflow_node_type_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.task_workflow_node_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_workflow_node_type_id_seq OWNER TO root;

--
-- Name: task_workflow_node_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.task_workflow_node_type_id_seq OWNED BY public.task_workflow_node_type.id;


--
-- Name: example_demo id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.example_demo ALTER COLUMN id SET DEFAULT nextval('public.example_demo_id_seq'::regclass);


--
-- Name: gen_table id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table ALTER COLUMN id SET DEFAULT nextval('public.gen_table_id_seq'::regclass);


--
-- Name: gen_table_column id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table_column ALTER COLUMN id SET DEFAULT nextval('public.gen_table_column_id_seq'::regclass);


--
-- Name: platform_email_config id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_config ALTER COLUMN id SET DEFAULT nextval('public.platform_email_config_id_seq'::regclass);


--
-- Name: platform_email_log id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_log ALTER COLUMN id SET DEFAULT nextval('public.platform_email_log_id_seq'::regclass);


--
-- Name: platform_email_template id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_template ALTER COLUMN id SET DEFAULT nextval('public.platform_email_template_id_seq'::regclass);


--
-- Name: platform_invoice id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_invoice ALTER COLUMN id SET DEFAULT nextval('public.platform_invoice_id_seq'::regclass);


--
-- Name: platform_menu id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_menu ALTER COLUMN id SET DEFAULT nextval('public.platform_menu_id_seq'::regclass);


--
-- Name: platform_order id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_order ALTER COLUMN id SET DEFAULT nextval('public.platform_order_id_seq'::regclass);


--
-- Name: platform_package id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package ALTER COLUMN id SET DEFAULT nextval('public.platform_package_id_seq'::regclass);


--
-- Name: platform_package_menu id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package_menu ALTER COLUMN id SET DEFAULT nextval('public.platform_package_menu_id_seq'::regclass);


--
-- Name: platform_package_plugin id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package_plugin ALTER COLUMN id SET DEFAULT nextval('public.platform_package_plugin_id_seq'::regclass);


--
-- Name: platform_payment_record id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_payment_record ALTER COLUMN id SET DEFAULT nextval('public.platform_payment_record_id_seq'::regclass);


--
-- Name: platform_plugin id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_plugin ALTER COLUMN id SET DEFAULT nextval('public.platform_plugin_id_seq'::regclass);


--
-- Name: platform_refund id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_refund ALTER COLUMN id SET DEFAULT nextval('public.platform_refund_id_seq'::regclass);


--
-- Name: platform_tenant id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_tenant ALTER COLUMN id SET DEFAULT nextval('public.platform_tenant_id_seq'::regclass);


--
-- Name: platform_tenant_plugin id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_tenant_plugin ALTER COLUMN id SET DEFAULT nextval('public.platform_tenant_plugin_id_seq'::regclass);


--
-- Name: platform_user_tenant id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_user_tenant ALTER COLUMN id SET DEFAULT nextval('public.platform_user_tenant_id_seq'::regclass);


--
-- Name: sys_dept id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept ALTER COLUMN id SET DEFAULT nextval('public.sys_dept_id_seq'::regclass);


--
-- Name: sys_dict_data id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_data ALTER COLUMN id SET DEFAULT nextval('public.sys_dict_data_id_seq'::regclass);


--
-- Name: sys_dict_type id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_type ALTER COLUMN id SET DEFAULT nextval('public.sys_dict_type_id_seq'::regclass);


--
-- Name: sys_login_log id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_login_log ALTER COLUMN id SET DEFAULT nextval('public.sys_login_log_id_seq'::regclass);


--
-- Name: sys_notice id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice ALTER COLUMN id SET DEFAULT nextval('public.sys_notice_id_seq'::regclass);


--
-- Name: sys_operation_log id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_operation_log ALTER COLUMN id SET DEFAULT nextval('public.sys_operation_log_id_seq'::regclass);


--
-- Name: sys_param id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_param ALTER COLUMN id SET DEFAULT nextval('public.sys_param_id_seq'::regclass);


--
-- Name: sys_position id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_position ALTER COLUMN id SET DEFAULT nextval('public.sys_position_id_seq'::regclass);


--
-- Name: sys_role id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role ALTER COLUMN id SET DEFAULT nextval('public.sys_role_id_seq'::regclass);


--
-- Name: sys_ticket id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_ticket ALTER COLUMN id SET DEFAULT nextval('public.sys_ticket_id_seq'::regclass);


--
-- Name: sys_user id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user ALTER COLUMN id SET DEFAULT nextval('public.sys_user_id_seq'::regclass);


--
-- Name: task_job id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_job ALTER COLUMN id SET DEFAULT nextval('public.task_job_id_seq'::regclass);


--
-- Name: task_node id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_node ALTER COLUMN id SET DEFAULT nextval('public.task_node_id_seq'::regclass);


--
-- Name: task_workflow id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow ALTER COLUMN id SET DEFAULT nextval('public.task_workflow_id_seq'::regclass);


--
-- Name: task_workflow_node_type id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type ALTER COLUMN id SET DEFAULT nextval('public.task_workflow_node_type_id_seq'::regclass);


--
-- Data for Name: apscheduler_jobs; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.apscheduler_jobs (id, next_run_time, job_state) FROM stdin;
\.


--
-- Data for Name: example_demo; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.example_demo (name, status, description, int_val, bigint_val, float_val, bool_val, date_val, time_val, datetime_val, text_val, json_val, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
用户管理模块	0	用户管理核心模块	15	15000	99.99	t	2025-06-01	09:00:00	2025-06-01 09:00:00	用户管理模块提供用户注册、登录、权限分配、个人中心等完整功能。	{"version": "1.0", "author": "admin", "tags": ["user", "auth"]}	1	9fa433e6-89cc-4649-933a-6cb3e2ac76cf	f	2026-06-21 18:12:31.258845	2026-06-21 18:12:31.258847	\N	1	\N	\N	\N
订单支付模块	0	订单与支付核心模块	28	300000	199.5	t	2025-06-15	14:30:00	2025-06-15 14:30:00	订单支付模块支持微信支付、支付宝、银行卡等多种支付方式，包含支付回调、退款处理等。	{"version": "2.1", "author": "payment-team", "tags": ["order", "payment", "refund"]}	2	8c84ccf4-42c7-4850-8fb6-e535d6fd26ed	f	2026-06-21 18:12:31.258851	2026-06-21 18:12:31.258852	\N	1	\N	\N	\N
消息通知模块	1	消息通知服务模块（开发中）	8	5000	0	f	2025-07-01	08:00:00	2025-07-01 08:00:00	消息通知模块支持站内信、邮件、短信等多渠道通知推送。	{"version": "0.9", "author": "dev-team", "tags": ["notification", "email", "sms"]}	3	40b6d070-d87c-4a2a-b944-c49900aa76c0	f	2026-06-21 18:12:31.258855	2026-06-21 18:12:31.258855	\N	1	\N	\N	\N
数据分析报表	0	高级数据分析与报表模块	42	1000000	499	t	2025-08-01	10:00:00	2025-08-01 10:00:00	数据分析报表模块提供可视化图表、数据导出、实时监控大屏等高级分析功能。	{"version": "3.0", "author": "data-team", "tags": ["analytics", "dashboard", "report", "chart"]}	4	b4e67d84-9900-459b-8965-ca12e931bbc3	f	2026-06-21 18:12:31.25886	2026-06-21 18:12:31.25886	\N	1	\N	\N	\N
文件存储服务	0	文件存储与 CDN 加速服务	20	50000	29.9	t	2025-09-01	16:00:00	2025-09-01 16:00:00	文件存储服务支持本地存储、阿里云OSS、腾讯云COS等多种存储后端，提供文件上传、下载、预览等接口。	{"version": "1.5", "author": "infra-team", "tags": ["storage", "oss", "upload"]}	5	09748759-0aaf-4adc-bc8d-da2b3fed7ff4	f	2026-06-21 18:12:31.258864	2026-06-21 18:12:31.258864	\N	1	\N	\N	\N
测试占位模块	1	仅用于测试空值处理	\N	\N	\N	t	\N	\N	\N	\N	null	6	49eade3f-ed47-485f-a41a-a41d26fdb463	f	2026-06-21 18:12:31.258867	2026-06-21 18:12:31.258867	\N	1	\N	\N	\N
\.


--
-- Data for Name: gen_table; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.gen_table (table_name, table_comment, class_name, package_name, module_name, business_name, function_name, sub_table_name, sub_table_fk_name, parent_menu_id, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
\.


--
-- Data for Name: gen_table_column; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.gen_table_column (column_name, column_comment, column_type, column_length, column_default, is_pk, is_increment, is_nullable, is_unique, python_type, python_field, is_insert, is_edit, is_list, is_query, query_type, html_type, dict_type, sort, table_id, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
\.


--
-- Data for Name: platform_email_config; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_email_config (name, smtp_host, smtp_port, smtp_user, smtp_password, from_name, use_tls, is_default, timeout, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time) FROM stdin;
默认SMTP	smtp.example.com	465	noreply@fastapiadmin.com	PLACEHOLDER_AES_ENCRYPTED	FastapiAdmin	t	t	30	0	平台默认SMTP配置	1	f3940d59-81a7-4b5b-8789-3ec7d786dd29	f	2026-06-21 18:12:31.124899	2026-06-21 18:12:31.124904	\N
\.


--
-- Data for Name: platform_email_log; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_email_log (config_id, template_code, to_email, to_name, subject, biz_type, error_msg, retry_count, tenant_id, sent_time, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, created_id, updated_id, deleted_id) FROM stdin;
\.


--
-- Data for Name: platform_email_template; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_email_template (name, template_code, subject, body_html, body_text, variables, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time) FROM stdin;
注册验证码	register_code	【FastapiAdmin】注册验证码	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#1a1a2e;margin-top:0;'>欢迎注册 FastapiAdmin</h2><p style='color:#666;font-size:15px;line-height:1.8;'>{{ username }} 您好：</p><p style='color:#666;font-size:15px;line-height:1.8;'>您的验证码是：</p><div style='background:linear-gradient(135deg,#667eea,#764ba2);padding:16px 24px;border-radius:6px;text-align:center;margin:20px 0;'><span style='color:#fff;font-size:28px;font-weight:bold;letter-spacing:6px;'>{{ code }}</span></div><p style='color:#999;font-size:13px;line-height:1.6;'>验证码 5 分钟内有效，请勿泄露给他人。</p><hr style='border:none;border-top:1px solid #eee;margin:24px 0;'><p style='color:#bbb;font-size:12px;text-align:center;'>此邮件由系统自动发送，请勿回复。</p></div></div>	欢迎注册 FastapiAdmin\n\n{{ username }} 您好：\n\n您的验证码是：{{ code }}\n\n验证码 5 分钟内有效，请勿泄露给他人。\n\n此邮件由系统自动发送，请勿回复。	{"username":"用户名","code":"验证码"}	0	用户注册发送邮箱验证码	1	e36b59d0-5097-4f71-9189-e39f1d29757e	f	2026-06-21 18:12:31.129875	2026-06-21 18:12:31.129878	\N
密码重置	reset_password	【FastapiAdmin】密码重置	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#1a1a2e;margin-top:0;'>密码重置</h2><p style='color:#666;font-size:15px;line-height:1.8;'>{{ username }} 您好：</p><p style='color:#666;font-size:15px;line-height:1.8;'>您正在申请重置密码，点击下方链接设置新密码（30 分钟内有效）：</p><div style='text-align:center;margin:24px 0;'><a href='{{ reset_link }}' style='display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:12px 32px;border-radius:6px;text-decoration:none;font-size:16px;font-weight:bold;'>重置密码</a></div><p style='color:#999;font-size:13px;'>如非本人操作，请忽略此邮件。</p><hr style='border:none;border-top:1px solid #eee;margin:24px 0;'><p style='color:#bbb;font-size:12px;text-align:center;'>此邮件由系统自动发送，请勿回复。</p></div></div>	密码重置\n\n{{ username }} 您好：\n\n您正在申请重置密码，请点击以下链接设置新密码（30 分钟内有效）：\n{{ reset_link }}\n\n如非本人操作，请忽略此邮件。\n\n此邮件由系统自动发送，请勿回复。	{"username":"用户名","reset_link":"密码重置链接"}	0	用户申请重置登录密码	2	5b5ee093-011c-4686-8585-72e9c7e62fae	f	2026-06-21 18:12:31.129882	2026-06-21 18:12:31.129883	\N
邮箱验证	email_verify	【FastapiAdmin】请验证您的邮箱	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#1a1a2e;margin-top:0;'>验证您的邮箱</h2><p style='color:#666;font-size:15px;line-height:1.8;'>{{ username }} 您好：</p><p style='color:#666;font-size:15px;line-height:1.8;'>感谢您注册 FastapiAdmin！请点击下方按钮完成邮箱验证（24 小时内有效）：</p><div style='text-align:center;margin:24px 0;'><a href='{{ verify_link }}' style='display:inline-block;background:linear-gradient(135deg,#27ae60,#2ecc71);color:#fff;padding:12px 32px;border-radius:6px;text-decoration:none;font-size:16px;font-weight:bold;'>验证邮箱</a></div><p style='color:#999;font-size:13px;'>如果按钮无法点击，请复制以下链接到浏览器：<br>{{ verify_link }}</p></div></div>	邮箱验证\n\n{{ username }} 您好：\n\n请点击以下链接完成邮箱验证（24 小时内有效）：\n{{ verify_link }}	{"username":"用户名","verify_link":"验证链接"}	0	新用户邮箱地址验证	3	272556f1-dfd7-4b2b-a9b9-34aba55362db	f	2026-06-21 18:12:31.129886	2026-06-21 18:12:31.129886	\N
工单回复通知	ticket_reply	【FastapiAdmin】工单回复通知 - {{ ticket_title }}	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#1a1a2e;margin-top:0;'>工单回复通知</h2><p style='color:#666;font-size:15px;line-height:1.8;'>您的工单 <strong>{{ ticket_title }}</strong> 收到新回复：</p><div style='background:#f8f9fb;border-left:4px solid #667eea;padding:16px 20px;margin:16px 0;border-radius:4px;'><p style='color:#444;font-size:14px;line-height:1.8;margin:0;'>{{ reply_content }}</p></div><p style='color:#999;font-size:13px;'>回复时间：{{ reply_time }}</p><div style='text-align:center;margin:24px 0;'><a href='{{ ticket_link }}' style='display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-size:14px;'>查看工单</a></div></div></div>	工单回复通知\n\n您的工单 {{ ticket_title }} 收到新回复：\n{{ reply_content }}\n\n回复时间：{{ reply_time }}\n查看工单：{{ ticket_link }}	{"ticket_title":"工单标题","reply_content":"回复内容","reply_time":"回复时间","ticket_link":"工单链接"}	0	工单被回复时通知提交人	4	096b984b-d8ff-43d0-b757-b25351eb6744	f	2026-06-21 18:12:31.129889	2026-06-21 18:12:31.12989	\N
套餐到期提醒	expiry_warning	【FastapiAdmin】套餐即将到期提醒	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#e74c3c;margin-top:0;'>套餐即将到期</h2><p style='color:#666;font-size:15px;line-height:1.8;'>尊敬的 {{ tenant_name }}：</p><p style='color:#666;font-size:15px;line-height:1.8;'>您的 <strong>{{ package_name }}</strong> 套餐将于 <strong style='color:#e74c3c;'>{{ expire_date }}</strong> 到期，剩余 <strong style='color:#e74c3c;'>{{ remaining_days }}</strong> 天。</p><p style='color:#666;font-size:15px;line-height:1.8;'>到期后部分功能将受限，请及时续费以保证服务正常使用。</p><div style='text-align:center;margin:24px 0;'><a href='{{ renew_link }}' style='display:inline-block;background:linear-gradient(135deg,#e74c3c,#c0392b);color:#fff;padding:12px 32px;border-radius:6px;text-decoration:none;font-size:16px;font-weight:bold;'>立即续费</a></div></div></div>	套餐即将到期\n\n尊敬的 {{ tenant_name }}：您的「{{ package_name }}」套餐将于 {{ expire_date }} 到期，剩余 {{ remaining_days }} 天。请及时续费。\n续费链接：{{ renew_link }}	{"tenant_name":"租户名称","package_name":"套餐名称","expire_date":"到期日期","remaining_days":"剩余天数","renew_link":"续费链接"}	0	套餐到期前7/3/1天发送提醒	5	bd68feec-fc3b-48c0-8908-56d065038c1c	f	2026-06-21 18:12:31.129893	2026-06-21 18:12:31.129893	\N
团队邀请	team_invite	【FastapiAdmin】{{ tenant_name }} 邀请您加入团队	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#1a1a2e;margin-top:0;'>团队邀请</h2><p style='color:#666;font-size:15px;line-height:1.8;'>您好：</p><p style='color:#666;font-size:15px;line-height:1.8;'><strong>{{ inviter_name }}</strong> 邀请您加入 <strong>{{ tenant_name }}</strong> 团队。</p><div style='text-align:center;margin:24px 0;'><a href='{{ invite_link }}' style='display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:12px 32px;border-radius:6px;text-decoration:none;font-size:16px;font-weight:bold;'>接受邀请</a></div><p style='color:#999;font-size:13px;'>链接 24 小时内有效。</p></div></div>	团队邀请\n\n您好：{{ inviter_name }} 邀请您加入 {{ tenant_name }} 团队。\n点击链接接受邀请：{{ invite_link }}\n链接 24 小时内有效。	{"tenant_name":"团队名称","inviter_name":"邀请人姓名","invite_link":"邀请链接"}	0	邀请新成员加入团队	6	21983e7a-3f4f-42ac-99fc-88c5df16f3af	f	2026-06-21 18:12:31.129895	2026-06-21 18:12:31.129896	\N
发票开具通知	invoice_issued	【FastapiAdmin】发票已开具 - {{ invoice_no }}	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#1a1a2e;margin-top:0;'>发票已开具</h2><p style='color:#666;font-size:15px;line-height:1.8;'>尊敬的客户：</p><p style='color:#666;font-size:15px;line-height:1.8;'>您的发票已开具完成：</p><table style='width:100%;border-collapse:collapse;margin:16px 0;'><tr><td style='padding:8px 12px;color:#888;'>发票号码</td><td style='padding:8px 12px;color:#333;'>{{ invoice_no }}</td></tr><tr style='background:#f8f9fb;'><td style='padding:8px 12px;color:#888;'>发票抬头</td><td style='padding:8px 12px;color:#333;'>{{ invoice_title }}</td></tr><tr><td style='padding:8px 12px;color:#888;'>开票金额</td><td style='padding:8px 12px;color:#333;font-weight:bold;'>¥{{ invoice_amount }}</td></tr></table><div style='text-align:center;margin:20px 0;'><a href='{{ pdf_link }}' style='display:inline-block;background:linear-gradient(135deg,#27ae60,#2ecc71);color:#fff;padding:12px 24px;border-radius:6px;text-decoration:none;font-size:15px;'>下载 PDF 电子发票</a></div></div></div>	发票已开具\n\n尊敬的客户：您的发票已开具完成。\n发票号码：{{ invoice_no }}\n发票抬头：{{ invoice_title }}\n开票金额：¥{{ invoice_amount }}\n下载 PDF：{{ pdf_link }}	{"invoice_no":"发票号","invoice_title":"发票抬头","invoice_amount":"开票金额","pdf_link":"PDF下载链接"}	0	发票开具完成通知客户	7	506b88b9-02a5-456b-9f2a-c765d6bf1287	f	2026-06-21 18:12:31.129898	2026-06-21 18:12:31.129899	\N
订单支付成功	order_paid	【FastapiAdmin】订单支付成功 - {{ order_no }}	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#27ae60;margin-top:0;'>✓ 订单支付成功</h2><p style='color:#666;font-size:15px;line-height:1.8;'>尊敬的 {{ username }}：</p><p style='color:#666;font-size:15px;line-height:1.8;'>您的订单已支付成功，详情如下：</p><table style='width:100%;border-collapse:collapse;margin:16px 0;'><tr><td style='padding:8px 12px;color:#888;'>订单号</td><td style='padding:8px 12px;color:#333;'>{{ order_no }}</td></tr><tr style='background:#f8f9fb;'><td style='padding:8px 12px;color:#888;'>订单金额</td><td style='padding:8px 12px;color:#333;font-weight:bold;'>¥{{ order_amount }}</td></tr><tr><td style='padding:8px 12px;color:#888;'>支付方式</td><td style='padding:8px 12px;color:#333;'>{{ pay_method }}</td></tr><tr style='background:#f8f9fb;'><td style='padding:8px 12px;color:#888;'>套餐名称</td><td style='padding:8px 12px;color:#333;'>{{ package_name }}</td></tr></table><p style='color:#999;font-size:13px;'>支付时间：{{ paid_time }}</p><div style='text-align:center;margin:24px 0;'><a href='{{ order_link }}' style='display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-size:14px;'>查看订单详情</a></div></div></div>	订单支付成功\n\n尊敬的 {{ username }}：\n\n您的订单已支付成功：\n订单号：{{ order_no }}\n订单金额：¥{{ order_amount }}\n支付方式：{{ pay_method }}\n套餐名称：{{ package_name }}\n支付时间：{{ paid_time }}\n\n查看订单：{{ order_link }}	{"username":"用户名","order_no":"订单号","order_amount":"订单金额","pay_method":"支付方式","package_name":"套餐名称","paid_time":"支付时间","order_link":"订单链接"}	0	订单支付完成通知	8	89d85df3-af61-4c85-aba7-c06a4f2b8563	f	2026-06-21 18:12:31.129902	2026-06-21 18:12:31.129902	\N
套餐升级成功	package_upgraded	【FastapiAdmin】套餐升级成功	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#1a1a2e;margin-top:0;'>套餐升级成功 🎉</h2><p style='color:#666;font-size:15px;line-height:1.8;'>尊敬的 {{ tenant_name }}：</p><p style='color:#666;font-size:15px;line-height:1.8;'>您的套餐已从 <strong>{{ old_package }}</strong> 升级为 <strong style='color:#27ae60;'>{{ new_package }}</strong>。</p><div style='background:#f8f9fb;border-left:4px solid #27ae60;padding:16px 20px;margin:16px 0;border-radius:4px;'><p style='color:#444;font-size:14px;line-height:1.8;margin:0;'>新套餐有效期至：<strong>{{ expire_date }}</strong></p></div><p style='color:#999;font-size:13px;'>升级时间：{{ upgrade_time }}</p><div style='text-align:center;margin:24px 0;'><a href='{{ console_link }}' style='display:inline-block;background:linear-gradient(135deg,#27ae60,#2ecc71);color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-size:14px;'>立即体验</a></div></div></div>	套餐升级成功\n\n尊敬的 {{ tenant_name }}：\n\n您的套餐已从 {{ old_package }} 升级为 {{ new_package }}。\n新套餐有效期至：{{ expire_date }}\n升级时间：{{ upgrade_time }}\n\n立即体验：{{ console_link }}	{"tenant_name":"租户名称","old_package":"原套餐","new_package":"新套餐","expire_date":"到期日期","upgrade_time":"升级时间","console_link":"控制台链接"}	0	租户套餐升级完成通知	9	33341757-d498-4a81-a181-e1ee3490a57b	f	2026-06-21 18:12:31.129905	2026-06-21 18:12:31.129905	\N
退款成功通知	refund_success	【FastapiAdmin】退款已到账 - {{ refund_no }}	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#27ae60;margin-top:0;'>退款已到账</h2><p style='color:#666;font-size:15px;line-height:1.8;'>尊敬的 {{ username }}：</p><p style='color:#666;font-size:15px;line-height:1.8;'>您的退款申请已处理完成：</p><table style='width:100%;border-collapse:collapse;margin:16px 0;'><tr><td style='padding:8px 12px;color:#888;'>退款单号</td><td style='padding:8px 12px;color:#333;'>{{ refund_no }}</td></tr><tr style='background:#f8f9fb;'><td style='padding:8px 12px;color:#888;'>原订单号</td><td style='padding:8px 12px;color:#333;'>{{ order_no }}</td></tr><tr><td style='padding:8px 12px;color:#888;'>退款金额</td><td style='padding:8px 12px;color:#e74c3c;font-weight:bold;'>¥{{ refund_amount }}</td></tr><tr style='background:#f8f9fb;'><td style='padding:8px 12px;color:#888;'>退回账户</td><td style='padding:8px 12px;color:#333;'>{{ refund_account }}</td></tr></table><p style='color:#999;font-size:13px;'>到账时间：{{ refund_time }}<br>预计 1-3 个工作日内到账，请注意查收。</p></div></div>	退款已到账\n\n尊敬的 {{ username }}：\n\n您的退款申请已处理完成：\n退款单号：{{ refund_no }}\n原订单号：{{ order_no }}\n退款金额：¥{{ refund_amount }}\n退回账户：{{ refund_account }}\n到账时间：{{ refund_time }}	{"username":"用户名","refund_no":"退款单号","order_no":"原订单号","refund_amount":"退款金额","refund_account":"退回账户","refund_time":"到账时间"}	0	用户退款成功通知	10	a23e5048-ee55-4e6b-b583-7ad87f75111f	f	2026-06-21 18:12:31.129908	2026-06-21 18:12:31.129908	\N
登录提醒	login_notify	【FastapiAdmin】账号登录提醒	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#1a1a2e;margin-top:0;'>账号登录提醒</h2><p style='color:#666;font-size:15px;line-height:1.8;'>{{ username }} 您好：</p><p style='color:#666;font-size:15px;line-height:1.8;'>您的账号于 <strong>{{ login_time }}</strong> 在 <strong>{{ login_location }}</strong> 登录。</p><table style='width:100%;border-collapse:collapse;margin:16px 0;'><tr><td style='padding:8px 12px;color:#888;'>登录 IP</td><td style='padding:8px 12px;color:#333;'>{{ login_ip }}</td></tr><tr style='background:#f8f9fb;'><td style='padding:8px 12px;color:#888;'>设备类型</td><td style='padding:8px 12px;color:#333;'>{{ device }}</td></tr><tr><td style='padding:8px 12px;color:#888;'>浏览器</td><td style='padding:8px 12px;color:#333;'>{{ browser }}</td></tr></table><p style='color:#e74c3c;font-size:13px;'>如非本人操作，请立即<a href='{{ change_pwd_link }}' style='color:#e74c3c;'>修改密码</a>并联系客服。</p><hr style='border:none;border-top:1px solid #eee;margin:24px 0;'><p style='color:#bbb;font-size:12px;text-align:center;'>此邮件由系统自动发送，请勿回复。</p></div></div>	账号登录提醒\n\n{{ username }} 您好：\n\n您的账号于 {{ login_time }} 在 {{ login_location }} 登录。\n登录 IP：{{ login_ip }}\n设备类型：{{ device }}\n浏览器：{{ browser }}\n\n如非本人操作，请立即修改密码并联系客服。	{"username":"用户名","login_time":"登录时间","login_location":"登录地点","login_ip":"登录IP","device":"设备类型","browser":"浏览器","change_pwd_link":"改密链接"}	0	异地/新设备登录提醒（安全）	11	2ea4ad52-e842-426b-b640-8935a3818d92	f	2026-06-21 18:12:31.129911	2026-06-21 18:12:31.129911	\N
密码已修改	password_changed	【FastapiAdmin】密码修改成功	<div style='max-width:600px;margin:0 auto;padding:20px;font-family:Arial,sans-serif;background:#f5f7fa;border-radius:8px;'><div style='background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'><h2 style='color:#27ae60;margin-top:0;'>密码修改成功</h2><p style='color:#666;font-size:15px;line-height:1.8;'>{{ username }} 您好：</p><p style='color:#666;font-size:15px;line-height:1.8;'>您的账号密码已于 <strong>{{ change_time }}</strong> 修改成功。</p><div style='background:#f8f9fb;border-left:4px solid #27ae60;padding:16px 20px;margin:16px 0;border-radius:4px;'><p style='color:#444;font-size:14px;line-height:1.8;margin:0;'>操作 IP：{{ change_ip }}<br>操作地点：{{ change_location }}</p></div><p style='color:#e74c3c;font-size:13px;'>如非本人操作，请立即联系客服冻结账号！</p><hr style='border:none;border-top:1px solid #eee;margin:24px 0;'><p style='color:#bbb;font-size:12px;text-align:center;'>此邮件由系统自动发送，请勿回复。</p></div></div>	密码修改成功\n\n{{ username }} 您好：\n\n您的账号密码已于 {{ change_time }} 修改成功。\n操作 IP：{{ change_ip }}\n操作地点：{{ change_location }}\n\n如非本人操作，请立即联系客服冻结账号！	{"username":"用户名","change_time":"修改时间","change_ip":"操作IP","change_location":"操作地点"}	0	用户修改密码成功通知	12	7ff519fe-dc8b-4d28-afe8-2a22c3727baa	f	2026-06-21 18:12:31.129914	2026-06-21 18:12:31.129914	\N
\.


--
-- Data for Name: platform_invoice; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_invoice (invoice_no, order_id, invoice_type, title, tax_no, bank_info, address_info, amount, tax_amount, pdf_url, oss_license_pdf_url, api_response, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
INV20260101001	1	vat_special	星辰科技有限公司	91440300MA5ABCDE12	中国工商银行深圳科技园支行 4000023409100123456	深圳市南山区科技园路1号 0755-88888888	29900	4485	/static/invoice/3/INV20260101001.pdf	/static/invoice/3/INV20260101001_license.pdf	\N	1	星辰科技-标准版年付发票（已开具）	1	94215250-61d4-4e9b-88f3-52935b43e4df	f	2026-06-21 18:12:31.154756	2026-06-21 18:12:31.154759	\N	3	\N	\N	\N
INV20260315001	2	vat_normal	星辰科技有限公司	\N	\N	\N	9900	1485	/static/invoice/3/INV20260315001.pdf	/static/invoice/3/INV20260315001_license.pdf	\N	1	星辰科技-AI助手发票（已开具）	2	de8416dc-409e-4dac-9864-b1090caa257f	f	2026-06-21 18:12:31.154763	2026-06-21 18:12:31.154764	\N	3	\N	\N	\N
INV20260601001	6	vat_normal	创新工坊	\N	\N	\N	29900	4485	\N	\N	\N	0	创新工坊-标准版月付发票（待开具）	3	237fa046-78ce-41c1-bc4b-4f8444e15330	f	2026-06-21 18:12:31.154767	2026-06-21 18:12:31.154767	\N	4	\N	\N	\N
INV20260610001	7	vat_normal	创新工坊	\N	\N	\N	4900	735	\N	\N	\N	0	创新工坊-数据大屏发票（待开具）	4	27124a02-eba4-49a3-8ca2-5d3a489ed103	f	2026-06-21 18:12:31.15477	2026-06-21 18:12:31.15477	\N	4	\N	\N	\N
\.


--
-- Data for Name: platform_menu; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_menu (name, type, "order", permission, icon, route_name, route_path, component_path, redirect, hidden, keep_alive, always_show, title, params, affix, client, link, is_iframe, is_hide_tab, active_path, show_badge, show_text_badge, scope, status, description, parent_id, id, uuid, is_deleted, created_time, updated_time, deleted_time) FROM stdin;
平台管理	1	1	\N	ri:building-4-line	Platform	/platform	\N	/platform/menu	f	t	t	平台管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	\N	1	ff3893d8-2b4f-4c73-9251-a6f3b7ae8690	f	2026-06-21 18:12:31.007321	2026-06-21 18:12:31.007332	\N
系统管理	1	2	\N	ri:settings-2-line	System	/system	\N	/system/dept	f	t	f	系统管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	\N	2	9da626b8-3e0b-469b-8e32-6ba098ed8f4d	f	2026-06-21 18:12:31.007367	2026-06-21 18:12:31.007368	\N
监控管理	1	3	\N	ri:computer-line	Monitor	/monitor	\N	/monitor/online	f	t	f	监控管理	null	f	pc	\N	f	f	\N	t	NEW	platform	0	初始化数据	\N	3	6cb60a55-2f24-4aa6-bde1-992d9c750227	f	2026-06-21 18:12:31.007373	2026-06-21 18:12:31.007373	\N
接口管理	1	4	\N	ri:file-text-line	Swagger	/swagger	\N	/swagger/docs	f	t	f	接口管理	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	\N	4	4eb8466b-0f51-4486-997b-cab905afb981	f	2026-06-21 18:12:31.007376	2026-06-21 18:12:31.007376	\N
代码管理	1	5	\N	ri:code-s-slash-line	Generator	/generator	\N	/generator/gencode	f	t	f	代码管理	null	f	pc	\N	f	f	\N	t	DEV	platform	0	代码管理	\N	5	44164b46-8ecc-4ccd-8d2c-8f813ed6d21f	f	2026-06-21 18:12:31.007379	2026-06-21 18:12:31.007379	\N
AI管理	1	7	\N	ri:chat-3-line	AI	/ai	\N	/ai/chat	f	t	f	AI管理	null	f	pc	\N	f	f	\N	t	HOT	platform	0	AI管理	\N	6	c44808bd-02dc-4ad2-bdc6-a9f31876c90f	f	2026-06-21 18:12:31.007382	2026-06-21 18:12:31.007382	\N
任务管理	1	8	\N	ri:tools-line	Task	/task	\N	/task/cronjob/job	f	t	f	任务管理	null	f	pc	\N	f	f	\N	t	BETA	platform	0	任务管理	\N	7	3c9e883d-d185-44d0-8389-72f4d61e02ae	f	2026-06-21 18:12:31.007385	2026-06-21 18:12:31.007385	\N
案例管理	1	9	\N	ri:menu-line	Example	/example	\N	/example/demo-center/demo	f	t	f	案例管理	null	f	pc	\N	f	f	\N	t	BETA	tenant	0	案例管理	\N	8	65bb4321-9c62-4ebf-85d5-07c43fe402fd	f	2026-06-21 18:12:31.007388	2026-06-21 18:12:31.007388	\N
首页	1	90		ri:home-4-line	AppHome	/app/home	\N	/app/home	f	t	t	首页	null	f	app	\N	f	f	\N	f	\N	tenant	0	APP 移动端-首页	\N	9	aaae5c24-49ba-45bb-992f-c39e9b51b9c5	f	2026-06-21 18:12:31.007391	2026-06-21 18:12:31.007391	\N
同事	1	91		ri:user-heart-line	AppColleague	/app/colleague	\N	/app/colleague	f	t	t	同事	null	f	app	\N	f	f	\N	f	\N	tenant	0	APP 移动端-同事	\N	10	eae9bb55-d5fb-43d1-9bb1-065cbdbfd90b	f	2026-06-21 18:12:31.007394	2026-06-21 18:12:31.007395	\N
打卡	1	92		ri:time-line	AppAttendance	/app/attendance	\N	/app/attendance	f	t	t	打卡	null	f	app	\N	f	f	\N	f	\N	tenant	0	APP 移动端-打卡	\N	11	ddf38b47-8f44-46b6-9303-375cae0fd10d	f	2026-06-21 18:12:31.007397	2026-06-21 18:12:31.007398	\N
消息	1	93		ri:message-3-line	AppMessage	/app/message	\N	/app/message	f	t	t	消息	null	f	app	\N	f	f	\N	f	\N	tenant	0	APP 移动端-消息	\N	12	9c080cea-2c7e-4a08-beb3-394447df3c85	f	2026-06-21 18:12:31.0074	2026-06-21 18:12:31.007401	\N
我的	1	94		ri:user-line	AppMine	/app/mine	\N	/app/mine	f	t	t	我的	null	f	app	\N	f	f	\N	f	\N	tenant	0	APP 移动端-我的	\N	13	ab69295a-591a-4bd4-ad65-ba1a813fc43e	f	2026-06-21 18:12:31.007403	2026-06-21 18:12:31.007404	\N
菜单管理	2	1	module_platform:menu:query	ri:menu-line	Menu	menu	module_platform/menu/index	\N	f	t	f	菜单管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	1	14	6bb8db4a-f156-4c6d-8910-132dd729fceb	f	2026-06-21 18:12:31.010885	2026-06-21 18:12:31.010889	\N
租户管理	2	2	module_system:tenant:query	ri:presentation-line	Tenant	tenant	module_platform/tenant/index	\N	f	t	f	租户管理	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	1	15	4ede7a12-f180-4f50-aae7-247e85ffb8db	f	2026-06-21 18:12:31.010893	2026-06-21 18:12:31.010894	\N
套餐管理	2	3	module_package:package:query	ri:vip-crown-2-line	Package	package	module_platform/package/index	\N	f	t	f	套餐管理	null	f	pc	\N	f	f	\N	f	\N	platform	0	套餐管理菜单	1	16	a27596e3-0aad-432f-8e55-6b6132f1d185	f	2026-06-21 18:12:31.010897	2026-06-21 18:12:31.010897	\N
邮件管理	2	5	module_platform:email:*	ri:mail-send-line	Email	email	module_platform/email/index	\N	f	t	f	邮件管理	null	f	pc	\N	f	f	\N	f	\N	platform	0	系统邮件服务管理	1	17	b3d1d80d-2a09-4099-a73b-adaf45c45de4	f	2026-06-21 18:12:31.0109	2026-06-21 18:12:31.0109	\N
订单管理	2	7	module_platform:order:query	ri:file-list-3-line	PlatformOrder	order	module_platform/order/index	\N	f	t	f	订单管理	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	1	18	f52e744c-0da1-41f0-9a64-a36ed7b6a38a	f	2026-06-21 18:12:31.010903	2026-06-21 18:12:31.010903	\N
发票管理	2	9	module_platform:invoice:query	ri:file-text-line	PlatformInvoice	invoice	module_platform/invoice/index	\N	f	t	f	发票管理	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	1	19	e2fc7d45-f6d7-4d62-b1b8-6d868be8e826	f	2026-06-21 18:12:31.010906	2026-06-21 18:12:31.010907	\N
租户工作台	2	13	module_platform:workspace:query	ri:briefcase-line	PlatformWorkspace	workspace	module_platform/self_service/index	\N	f	t	f	租户工作台	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	1	20	d48b1997-6641-4ec5-b5b2-fdd0b5cba04d	f	2026-06-21 18:12:31.010909	2026-06-21 18:12:31.01091	\N
插件市场	2	14	module_platform:plugin:query	ri:store-2-line	PluginMarket	plugin-market	module_platform/plugin/index	\N	f	t	f	插件市场	null	f	pc	\N	f	f	\N	t	NEW	platform	0	初始化数据	1	21	d9edc48b-2964-41d3-ae5a-6b0e68a2c571	f	2026-06-21 18:12:31.010912	2026-06-21 18:12:31.010913	\N
字典管理	2	1	module_system:dict_type:query	ri:book-2-line	Dict	dict	module_system/dict/index	\N	f	t	f	字典管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	2	22	8c5eec6d-1c6c-47bb-9be3-c1287c07a8ec	f	2026-06-21 18:12:31.010915	2026-06-21 18:12:31.010916	\N
参数管理	2	2	module_system:param:query	ri:settings-3-line	Params	param	module_system/params/index	\N	f	t	f	参数管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	2	23	189e1d71-9c8d-45d9-9969-23f98366718b	f	2026-06-21 18:12:31.010918	2026-06-21 18:12:31.010919	\N
部门管理	2	3	module_system:dept:query	ri:node-tree	Dept	dept	module_system/dept/index	\N	f	t	f	部门管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	2	24	b2b29598-7877-4b49-8bfe-85f378fade61	f	2026-06-21 18:12:31.010921	2026-06-21 18:12:31.010922	\N
岗位管理	2	4	module_system:position:query	ri:map-pin-line	Position	position	module_system/position/index	\N	f	t	f	岗位管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	2	25	26425710-604d-4b59-8557-5c61aedef3fa	f	2026-06-21 18:12:31.010924	2026-06-21 18:12:31.010925	\N
角色管理	2	5	module_system:role:query	ri:admin-line	Role	role	module_system/role/index	\N	f	t	f	角色管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	2	26	a8dfe1c7-b285-4080-a794-c17464f94330	f	2026-06-21 18:12:31.010927	2026-06-21 18:12:31.010928	\N
用户管理	2	6	module_system:user:query	ri:user-line	User	user	module_system/user/index	\N	f	t	f	用户管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	2	27	aeea1edd-c5d1-448d-a180-b893fc12bfe3	f	2026-06-21 18:12:31.01093	2026-06-21 18:12:31.010931	\N
日志管理	2	7	module_system:log:query	ri:focus-3-line	Log	log	module_system/log/index	\N	f	t	f	日志管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	2	28	71512ff8-5b93-4d15-843c-58d4f7cbd7df	f	2026-06-21 18:12:31.010933	2026-06-21 18:12:31.010934	\N
公告管理	2	8	module_system:notice:query	ri:notification-3-line	Notice	notice	module_system/notice/index	\N	f	t	f	公告管理	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	2	29	30b939aa-7b5c-40ec-97f9-740209d89716	f	2026-06-21 18:12:31.010936	2026-06-21 18:12:31.010936	\N
工单管理	2	10	module_system:ticket:query	ri:feedback-line	ModuleTicket	ticket	module_system/ticket/index	\N	f	t	f	工单管理	null	f	pc	\N	f	f	\N	t	NEW	tenant	0	初始化数据	2	30	30a122b1-799c-4359-a093-609885cd4bad	f	2026-06-21 18:12:31.010939	2026-06-21 18:12:31.010939	\N
系统配置	3	99	module_system:config:update	\N	\N	\N	\N	\N	f	t	f	系统配置	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	2	31	9d3968cc-ec25-4ed1-b0cc-f354eac0757d	f	2026-06-21 18:12:31.010942	2026-06-21 18:12:31.010942	\N
在线用户	2	1	module_monitor:online:query	ri:customer-service-2-line	MonitorOnline	online	module_monitor/online/index	\N	f	t	f	在线用户	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	3	32	3d8889ca-29f8-4536-a2de-6f7dfad6297c	f	2026-06-21 18:12:31.010945	2026-06-21 18:12:31.010945	\N
服务器监控	2	2	module_monitor:server:query	ri:dashboard-3-line	MonitorServer	server	module_monitor/server/index	\N	f	t	f	服务器监控	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	3	33	c20afd98-d28e-4f21-9fc0-0762ff0fd14b	f	2026-06-21 18:12:31.010948	2026-06-21 18:12:31.010948	\N
缓存监控	2	3	module_monitor:cache:query	ri:timer-flash-line	MonitorCache	cache	module_monitor/cache/index	\N	f	t	f	缓存监控	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	3	34	a28d2a19-4dda-48d9-9857-e981967f2f04	f	2026-06-21 18:12:31.010951	2026-06-21 18:12:31.010951	\N
文件管理	2	4	module_monitor:resource:query	ri:folder-5-line	Resource	resource	module_monitor/resource/index	\N	f	t	f	文件管理	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	3	35	ebf78c17-eb5b-4b85-b83d-58697876a276	f	2026-06-21 18:12:31.010954	2026-06-21 18:12:31.010954	\N
Swagger文档	4	1	module_swagger:docs:query	ri:plug-line	Docs	docs	module_swagger/docs/index	\N	f	t	f	Swagger文档	null	f	pc	/api/v1/docs	t	f	\N	f	\N	platform	0	初始化数据	4	36	4e686928-ca35-4440-8234-84a3ef25fa2a	f	2026-06-21 18:12:31.010957	2026-06-21 18:12:31.010957	\N
Redoc文档	4	2	module_swagger:redoc:query	ri:file-text-line	Redoc	redoc	module_swagger/redoc/index	\N	f	t	f	Redoc文档	null	f	pc	/api/v1/redoc	t	f	\N	f	\N	platform	0	初始化数据	4	37	c230348e-e6ed-4a84-8b9b-e72d14219075	f	2026-06-21 18:12:31.01096	2026-06-21 18:12:31.01096	\N
代码生成	2	1	module_generator:gencode:query	ri:code-s-slash-line	GenCode	gencode	module_generator/gencode/index	\N	f	t	f	代码生成	null	f	pc	\N	f	f	\N	f	\N	platform	0	代码生成	5	38	b00a5576-3502-4370-accd-2875f75ed6f8	f	2026-06-21 18:12:31.010963	2026-06-21 18:12:31.010963	\N
AI智能助手	2	1	module_ai:chat:query	ri:message-2-line	Chat	chat	module_ai/chat/index	\N	f	t	f	AI智能助手	null	f	pc	\N	f	f	\N	f	\N	platform	0	AI智能助手	6	39	767efb39-1301-4aec-a459-1e969d0bcb84	f	2026-06-21 18:12:31.010966	2026-06-21 18:12:31.010966	\N
会话记忆	2	2	module_ai:chat:query	ri:chat-3-line	Memory	memory	module_ai/memory/index	\N	f	t	f	会话记忆	null	f	pc	\N	f	f	\N	f	\N	platform	0	会话记忆管理	6	40	c7022a0d-8574-4bc4-9be7-01fcec2609dc	f	2026-06-21 18:12:31.010969	2026-06-21 18:12:31.010969	\N
定时任务	1	1	\N	ri:timer-line	Cronjob	cronjob	\N	/task/cronjob/job	f	t	t	定时任务	null	f	pc	\N	f	f	\N	f	\N	platform	0	APScheduler 调度器与任务节点	7	41	c26e803f-cc05-42e4-9c0d-92863157224d	f	2026-06-21 18:12:31.010972	2026-06-21 18:12:31.010973	\N
工作流	1	2	\N	ri:tools-line	WorkflowMgr	workflow-mgr	\N	/task/workflow/definition	f	t	t	工作流	null	f	pc	\N	f	f	\N	f	\N	platform	0	流程编排与编排节点类型	7	42	ef7c77fb-7b80-4d64-99c6-5115ecdbb4cb	f	2026-06-21 18:12:31.010975	2026-06-21 18:12:31.010976	\N
示例中心	1	1	\N	ri:apps-line	DemoCenter	demo-center	\N	/example/demo-center/demo	f	t	f	示例中心	null	f	pc	\N	f	f	\N	f	\N	tenant	0	示例中心	8	43	96193341-d8eb-494c-b9cb-0bbb595f3215	f	2026-06-21 18:12:31.010978	2026-06-21 18:12:31.010979	\N
新增	3	1	module_platform:menu:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	14	44	f19961c6-4548-4f1b-bb6d-daffb55a48cb	f	2026-06-21 18:12:31.016684	2026-06-21 18:12:31.016688	\N
编辑	3	2	module_platform:menu:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	14	45	057fa4ce-907b-4613-9fb6-e1bc28bf6c58	f	2026-06-21 18:12:31.016694	2026-06-21 18:12:31.016694	\N
删除	3	3	module_platform:menu:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	14	46	125e3b67-0690-4917-b08e-b9b62a5f0c32	f	2026-06-21 18:12:31.016698	2026-06-21 18:12:31.016698	\N
状态变更	3	4	module_platform:menu:patch	\N	\N	\N	\N	\N	f	t	f	状态变更	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	14	47	82d4243d-a3e8-4c59-a51c-5a0b7598463d	f	2026-06-21 18:12:31.016701	2026-06-21 18:12:31.016701	\N
详情	3	5	module_platform:menu:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	14	48	f85f129f-e574-4e69-9e1f-3f7e279d9655	f	2026-06-21 18:12:31.016704	2026-06-21 18:12:31.016704	\N
查询	3	6	module_platform:menu:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	14	49	c7e2052c-e807-414e-b05a-4f6f3f217c77	f	2026-06-21 18:12:31.016707	2026-06-21 18:12:31.016707	\N
新增	3	1	module_system:tenant:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	15	50	7312433b-b3a5-4dc9-b195-a9e737f4681c	f	2026-06-21 18:12:31.016752	2026-06-21 18:12:31.016754	\N
编辑	3	2	module_system:tenant:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	15	51	a8e03365-5bfd-4be1-b5f5-01b83c8a6979	f	2026-06-21 18:12:31.016764	2026-06-21 18:12:31.016765	\N
删除	3	3	module_system:tenant:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	15	52	0974ef7c-16f9-41a6-bbc0-f9a6cbd2fac9	f	2026-06-21 18:12:31.016769	2026-06-21 18:12:31.016769	\N
状态变更	3	4	module_system:tenant:patch	\N	\N	\N	\N	\N	f	t	f	状态变更	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	15	53	3b283331-e1f3-492f-ad3f-251fc3371c40	f	2026-06-21 18:12:31.016772	2026-06-21 18:12:31.016773	\N
详情	3	5	module_system:tenant:query	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	15	54	02269bbd-ddd2-49ed-b447-55303bdae59f	f	2026-06-21 18:12:31.016775	2026-06-21 18:12:31.016776	\N
查询	3	6	module_system:tenant:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	15	55	4e44e6ac-e7ca-4e32-bc4a-70fd73c6dfc4	f	2026-06-21 18:12:31.016778	2026-06-21 18:12:31.016779	\N
配置管理	3	11	module_system:tenant:update	\N	\N	\N	\N	\N	f	t	f	配置管理	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	15	56	8616438b-97a5-49b7-821e-9403e3ea9bf8	f	2026-06-21 18:12:31.016782	2026-06-21 18:12:31.016782	\N
新增	3	1	module_package:package:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	platform	0	\N	16	57	ec9af271-a7c9-401c-b2b8-b128c30c717f	f	2026-06-21 18:12:31.016785	2026-06-21 18:12:31.016785	\N
编辑	3	2	module_package:package:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	platform	0	\N	16	58	d8f592e7-29fe-4bee-8db9-f08c3790f2b6	f	2026-06-21 18:12:31.016788	2026-06-21 18:12:31.016788	\N
删除	3	3	module_package:package:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	platform	0	\N	16	59	5bd0fe61-3a42-4f73-9e13-0100983c1c20	f	2026-06-21 18:12:31.016791	2026-06-21 18:12:31.016791	\N
查询	3	4	module_package:package:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	platform	0	\N	16	60	ab4c5806-4f19-47be-ad42-4899b0b4171b	f	2026-06-21 18:12:31.016794	2026-06-21 18:12:31.016794	\N
租户查询套餐	3	5	tenant:package:query	\N	\N	\N	\N	\N	t	t	f	租户查询套餐	null	f	pc	\N	f	f	\N	f	\N	platform	0	\N	16	61	41cc512c-190d-440a-86de-bd419164b8a2	f	2026-06-21 18:12:31.016796	2026-06-21 18:12:31.016797	\N
发件配置	3	1	module_platform:email:update	\N	EmailConfig	\N	\N	\N	f	t	f	\N	\N	f	pc	\N	f	f	\N	f	\N	platform	0	\N	17	62	a78e4d76-8efa-4a4c-9eaf-cc327857a64e	f	2026-06-21 18:12:31.020182	2026-06-21 18:12:31.020185	\N
邮件模板	3	2	module_platform:email:query	\N	EmailTemplate	\N	\N	\N	f	t	f	\N	\N	f	pc	\N	f	f	\N	f	\N	platform	0	\N	17	63	7fbd2909-b80b-47e5-907c-5b7b1ab5f151	f	2026-06-21 18:12:31.02019	2026-06-21 18:12:31.02019	\N
发送邮件	3	3	module_platform:email:update	\N	EmailSend	\N	\N	\N	f	t	f	\N	\N	f	pc	\N	f	f	\N	f	\N	platform	0	\N	17	64	c2ddcd74-761a-4fc1-bf3e-fcd34758202a	f	2026-06-21 18:12:31.020193	2026-06-21 18:12:31.020194	\N
发送日志	3	4	module_platform:email:query	\N	EmailLog	\N	\N	\N	f	t	f	\N	\N	f	pc	\N	f	f	\N	f	\N	platform	0	\N	17	65	d38964dd-1e6d-4619-b31b-2b8b5b3b69f0	f	2026-06-21 18:12:31.020197	2026-06-21 18:12:31.020197	\N
查询	3	1	module_platform:order:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	18	66	51997123-fe37-4a97-9dd0-15e51f5b2468	f	2026-06-21 18:12:31.023158	2026-06-21 18:12:31.023161	\N
新增	3	2	module_platform:order:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	18	67	fe07294a-6d79-442b-a86d-ada4cb2314e8	f	2026-06-21 18:12:31.023165	2026-06-21 18:12:31.023165	\N
取消订单	3	3	module_platform:order:update	\N	\N	\N	\N	\N	f	t	f	取消订单	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	18	68	153e4911-9138-4e9d-bc49-c036cc6ff37d	f	2026-06-21 18:12:31.023168	2026-06-21 18:12:31.023169	\N
租户创建订单	3	4	tenant:order:create	\N	\N	\N	\N	\N	t	t	f	租户创建订单	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	18	69	689f271f-9205-4edf-96c7-9fbad8cd6cbd	f	2026-06-21 18:12:31.023171	2026-06-21 18:12:31.023172	\N
租户查询订单	3	5	tenant:order:query	\N	\N	\N	\N	\N	t	t	f	租户查询订单	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	18	70	50ae0ed4-2102-4a65-89c3-f3bc23883d38	f	2026-06-21 18:12:31.023174	2026-06-21 18:12:31.023174	\N
租户申请退款	3	6	tenant:order:refund	\N	\N	\N	\N	\N	t	t	f	租户申请退款	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	18	71	a008ce5c-07f4-4913-ac50-ac32626861b0	f	2026-06-21 18:12:31.023177	2026-06-21 18:12:31.023177	\N
查询	3	1	module_platform:invoice:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	19	72	4ff4eabc-f0a5-4531-9d7e-e141980950ee	f	2026-06-21 18:12:31.02318	2026-06-21 18:12:31.02318	\N
新增	3	2	module_platform:invoice:update	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	19	73	6f7bb882-924d-42f7-b904-9a115e75c583	f	2026-06-21 18:12:31.023183	2026-06-21 18:12:31.023184	\N
作废发票	3	3	module_platform:invoice:update	\N	\N	\N	\N	\N	f	t	f	作废发票	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	19	74	c81cff52-999b-4de9-9cd0-20c1ace63d90	f	2026-06-21 18:12:31.023186	2026-06-21 18:12:31.023187	\N
查询	3	1	module_platform:workspace:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	20	75	e9e3d47c-c443-404a-9c30-d3297d020b4f	f	2026-06-21 18:12:31.023189	2026-06-21 18:12:31.023189	\N
查询	3	1	module_platform:plugin:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	21	76	7c2d550d-d053-43bf-b18f-fdbc68c6f40e	f	2026-06-21 18:12:31.023192	2026-06-21 18:12:31.023192	\N
安装	3	2	module_platform:plugin:install	\N	\N	\N	\N	\N	f	t	f	安装	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	21	77	6537489a-2598-4870-af1b-770d67dba4ae	f	2026-06-21 18:12:31.023195	2026-06-21 18:12:31.023195	\N
卸载	3	3	module_platform:plugin:uninstall	\N	\N	\N	\N	\N	f	t	f	卸载	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	21	78	909b1fa3-9c92-4536-8031-d81f4484059d	f	2026-06-21 18:12:31.023198	2026-06-21 18:12:31.023198	\N
新增	3	4	module_platform:plugin:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	21	79	3caac79d-e718-43c3-b96f-7788899f3b86	f	2026-06-21 18:12:31.023201	2026-06-21 18:12:31.023202	\N
编辑	3	5	module_platform:plugin:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	21	80	d9a64b4d-e61f-4dda-a05f-0856c468becf	f	2026-06-21 18:12:31.023205	2026-06-21 18:12:31.023205	\N
删除	3	6	module_platform:plugin:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	21	81	9c510743-356a-4d05-a8e4-80a0d8637fe0	f	2026-06-21 18:12:31.023207	2026-06-21 18:12:31.023208	\N
启用/禁用	3	7	module_platform:plugin:toggle	\N	\N	\N	\N	\N	f	t	f	启用/禁用	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	21	82	52df270f-3753-41c0-bcdc-4f1575264b8f	f	2026-06-21 18:12:31.02321	2026-06-21 18:12:31.023211	\N
重新加载	3	8	module_platform:plugin:reload	\N	\N	\N	\N	\N	f	t	f	重新加载	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	21	83	ee9965cb-b574-412f-ab5e-590c402f7c64	f	2026-06-21 18:12:31.023213	2026-06-21 18:12:31.023214	\N
新增	3	1	module_system:dict_type:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	84	22edd335-87ad-4bc9-8f75-ca922257c634	f	2026-06-21 18:12:31.023216	2026-06-21 18:12:31.023216	\N
编辑	3	2	module_system:dict_type:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	85	ff026d52-85bf-43b8-8aa7-45c357510182	f	2026-06-21 18:12:31.023219	2026-06-21 18:12:31.02322	\N
删除	3	3	module_system:dict_type:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	86	c8da1fa6-ee96-4a8a-a58a-f39d6c2cbd4d	f	2026-06-21 18:12:31.023222	2026-06-21 18:12:31.023222	\N
导出	3	4	module_system:dict_type:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	87	7a93d0e9-9cef-4c23-ad8a-d3c1549a6edd	f	2026-06-21 18:12:31.023225	2026-06-21 18:12:31.023225	\N
状态变更	3	5	module_system:dict_type:patch	\N	\N	\N	\N	\N	f	t	f	状态变更	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	88	7efe25b5-a0c8-45bd-97a5-3d02159889d0	f	2026-06-21 18:12:31.023228	2026-06-21 18:12:31.023228	\N
查询	3	6	module_system:dict_data:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	89	d9bf628e-c290-417f-a0a9-fa23623edff4	f	2026-06-21 18:12:31.023231	2026-06-21 18:12:31.023231	\N
新增	3	7	module_system:dict_data:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	90	7faebaa1-719e-400a-a7b4-8ab4dafe20cd	f	2026-06-21 18:12:31.023233	2026-06-21 18:12:31.023234	\N
编辑	3	8	module_system:dict_data:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	91	19d1fb98-95cd-4ac0-bfb4-738cafaebb56	f	2026-06-21 18:12:31.023236	2026-06-21 18:12:31.023237	\N
删除	3	9	module_system:dict_data:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	92	b969520e-c7ed-4b49-a6ed-60e8d611ba67	f	2026-06-21 18:12:31.023239	2026-06-21 18:12:31.02324	\N
导出	3	10	module_system:dict_data:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	93	0b035fe5-7585-4f89-920e-97f47a587a5b	f	2026-06-21 18:12:31.023242	2026-06-21 18:12:31.023243	\N
状态变更	3	11	module_system:dict_data:patch	\N	\N	\N	\N	\N	f	t	f	状态变更	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	94	00c763ae-72c7-42e7-98b7-81a532fe2f8f	f	2026-06-21 18:12:31.023246	2026-06-21 18:12:31.023246	\N
详情	3	12	module_system:dict_type:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	95	741ff094-af8d-4d0d-a2dc-7cb9e99ee3f8	f	2026-06-21 18:12:31.023249	2026-06-21 18:12:31.023249	\N
查询	3	13	module_system:dict_type:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	96	7a179962-e893-4ca0-a5a6-cba094d4266a	f	2026-06-21 18:12:31.023251	2026-06-21 18:12:31.023252	\N
详情	3	14	module_system:dict_data:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	22	97	7a2cd2fb-f47a-415a-9878-8ff427ae32d7	f	2026-06-21 18:12:31.023254	2026-06-21 18:12:31.023255	\N
新增	3	1	module_system:param:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	23	98	9e632811-0714-406e-bc14-8d50a8daab59	f	2026-06-21 18:12:31.023257	2026-06-21 18:12:31.023257	\N
编辑	3	2	module_system:param:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	23	99	1c6a24c8-2fb7-4865-9c46-a21bc5fdcddb	f	2026-06-21 18:12:31.02326	2026-06-21 18:12:31.02326	\N
删除	3	3	module_system:param:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	23	100	46625e5f-6413-4f1d-80d9-d9f2ef9aa4df	f	2026-06-21 18:12:31.023263	2026-06-21 18:12:31.023263	\N
导出	3	4	module_system:param:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	23	101	56708134-5cd0-4db3-9a39-11e7729fb417	f	2026-06-21 18:12:31.023266	2026-06-21 18:12:31.023266	\N
参数上传	3	5	module_system:param:upload	\N	\N	\N	\N	\N	f	t	f	参数上传	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	23	102	90bb7ea6-643f-4b6e-a86c-2b13920fae8b	f	2026-06-21 18:12:31.023269	2026-06-21 18:12:31.023269	\N
详情	3	6	module_system:param:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	23	103	1bb19608-1c93-4bd3-b6c4-5d3c8a7025e6	f	2026-06-21 18:12:31.023271	2026-06-21 18:12:31.023272	\N
查询	3	7	module_system:param:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	23	104	50cafcda-18cc-472c-ab93-b340965ef428	f	2026-06-21 18:12:31.023274	2026-06-21 18:12:31.023275	\N
批量操作	3	8	module_system:param:patch	\N	\N	\N	\N	\N	f	t	f	批量操作	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	23	105	ed5d8c03-d5ea-4bec-bd2f-067b7f188961	f	2026-06-21 18:12:31.023277	2026-06-21 18:12:31.023278	\N
新增	3	1	module_system:dept:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	24	106	2b2a9911-3e5a-4742-a5ee-2bb2171e13fd	f	2026-06-21 18:12:31.02328	2026-06-21 18:12:31.023281	\N
编辑	3	2	module_system:dept:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	24	107	78fbf1a5-01e2-4a3e-98cd-2fe87b66c47b	f	2026-06-21 18:12:31.023283	2026-06-21 18:12:31.023284	\N
删除	3	3	module_system:dept:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	24	108	fd59bac7-8a37-4b74-ac20-34f38423cabb	f	2026-06-21 18:12:31.023286	2026-06-21 18:12:31.023287	\N
状态变更	3	4	module_system:dept:patch	\N	\N	\N	\N	\N	f	t	f	状态变更	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	24	109	63c7e00a-da0d-4343-845c-ccada01507f7	f	2026-06-21 18:12:31.023289	2026-06-21 18:12:31.02329	\N
详情	3	5	module_system:dept:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	24	110	0257981c-8018-4bbd-9f46-049ccb4eadc1	f	2026-06-21 18:12:31.023292	2026-06-21 18:12:31.023293	\N
查询	3	6	module_system:dept:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	24	111	75a63855-aa6c-45c0-85ab-c617c06fb4c2	f	2026-06-21 18:12:31.023295	2026-06-21 18:12:31.023296	\N
新增	3	1	module_system:position:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	25	112	020ac945-2217-4173-b6cf-f8abac7b2c68	f	2026-06-21 18:12:31.023298	2026-06-21 18:12:31.023299	\N
编辑	3	2	module_system:position:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	25	113	cdd4e6d4-6781-47d7-b2c1-57089b92e493	f	2026-06-21 18:12:31.023301	2026-06-21 18:12:31.023301	\N
删除	3	3	module_system:position:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	25	114	5de5a69d-26cb-4831-ab72-e5862d288e75	f	2026-06-21 18:12:31.023304	2026-06-21 18:12:31.023304	\N
状态变更	3	4	module_system:position:patch	\N	\N	\N	\N	\N	f	t	f	状态变更	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	25	115	f6d81c0f-c492-4244-862e-16a0838b7a93	f	2026-06-21 18:12:31.023307	2026-06-21 18:12:31.023307	\N
导出	3	5	module_system:position:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	25	116	65880e3c-d86b-4a17-b4bd-dcad59ffd880	f	2026-06-21 18:12:31.02331	2026-06-21 18:12:31.02331	\N
详情	3	6	module_system:position:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	25	117	cef225e6-e20e-425a-87e9-5ae9bee01418	f	2026-06-21 18:12:31.023313	2026-06-21 18:12:31.023313	\N
查询	3	7	module_system:position:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	25	118	72583150-10e7-4132-8bfb-a1f3d75995aa	f	2026-06-21 18:12:31.023315	2026-06-21 18:12:31.023316	\N
新增	3	1	module_system:role:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	26	119	2ce935d5-50f2-4e43-80bd-303e5f1c3d32	f	2026-06-21 18:12:31.023318	2026-06-21 18:12:31.023319	\N
编辑	3	2	module_system:role:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	26	120	38fea98f-773b-4f36-8650-48bf7886d390	f	2026-06-21 18:12:31.023321	2026-06-21 18:12:31.023321	\N
删除	3	3	module_system:role:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	26	121	f2c0218e-538c-4971-afe3-bcb9778062bb	f	2026-06-21 18:12:31.023324	2026-06-21 18:12:31.023324	\N
状态变更	3	4	module_system:role:patch	\N	\N	\N	\N	\N	f	t	f	状态变更	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	26	122	bdd5a2aa-d260-41f0-8876-57df7f175e0d	f	2026-06-21 18:12:31.023327	2026-06-21 18:12:31.023327	\N
导出	3	5	module_system:role:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	26	123	25499731-f870-4276-a1f8-8f36162c3365	f	2026-06-21 18:12:31.02333	2026-06-21 18:12:31.02333	\N
详情	3	6	module_system:role:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	26	124	3a9a9fcf-51f4-47e0-a4f7-855c8253e987	f	2026-06-21 18:12:31.023332	2026-06-21 18:12:31.023333	\N
查询	3	7	module_system:role:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	26	125	626efae2-1050-4983-85f1-0cbe5a01dfde	f	2026-06-21 18:12:31.023335	2026-06-21 18:12:31.023336	\N
分配权限	3	8	module_system:role:permission	\N	\N	\N	\N	\N	f	t	f	分配权限	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	26	126	4620c2ad-f433-433c-bc45-aad055eb2bb7	f	2026-06-21 18:12:31.023338	2026-06-21 18:12:31.023338	\N
新增	3	1	module_system:user:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	27	127	9219409d-99b6-4795-9c02-51a341b57bd2	f	2026-06-21 18:12:31.023341	2026-06-21 18:12:31.023341	\N
编辑	3	2	module_system:user:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	27	128	14cf862a-4989-45c5-91c0-b8d0a181c7d4	f	2026-06-21 18:12:31.023344	2026-06-21 18:12:31.023344	\N
删除	3	3	module_system:user:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	27	129	876dd27e-f9ea-4745-acd6-acc6147b9fb3	f	2026-06-21 18:12:31.023347	2026-06-21 18:12:31.023347	\N
状态变更	3	4	module_system:user:patch	\N	\N	\N	\N	\N	f	t	f	状态变更	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	27	130	0fbd86dc-0019-484f-a484-2aee9bd14851	f	2026-06-21 18:12:31.02335	2026-06-21 18:12:31.02335	\N
导出	3	5	module_system:user:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	27	131	4be0fab3-9a07-471f-ab8f-189d9514cba6	f	2026-06-21 18:12:31.023352	2026-06-21 18:12:31.023353	\N
导入	3	6	module_system:user:import	\N	\N	\N	\N	\N	f	t	f	导入	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	27	132	7a7e5693-ca11-4f34-85d5-d3a1459ac2a5	f	2026-06-21 18:12:31.023355	2026-06-21 18:12:31.023356	\N
下载导入模板	3	7	module_system:user:download	\N	\N	\N	\N	\N	f	t	f	下载导入模板	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	27	133	42bffd6f-1fb4-4599-9bcc-cd4da056339f	f	2026-06-21 18:12:31.023358	2026-06-21 18:12:31.023359	\N
详情	3	8	module_system:user:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	27	134	ed425c47-86da-4019-8e19-931ba0a14b9e	f	2026-06-21 18:12:31.023361	2026-06-21 18:12:31.023361	\N
查询	3	9	module_system:user:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	27	135	5ef48f58-7f4f-4c5c-8dcb-171d965092b5	f	2026-06-21 18:12:31.023364	2026-06-21 18:12:31.023364	\N
删除	3	1	module_system:log:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	28	136	58d96c38-2a0e-48ae-a70f-4a0507f4be29	f	2026-06-21 18:12:31.023367	2026-06-21 18:12:31.023367	\N
导出	3	2	module_system:log:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	28	137	d25b16b9-820d-4222-a4a0-df774dff0176	f	2026-06-21 18:12:31.02337	2026-06-21 18:12:31.02337	\N
详情	3	3	module_system:log:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	28	138	757001fd-13a9-414d-af73-36bc59f22bce	f	2026-06-21 18:12:31.023372	2026-06-21 18:12:31.023373	\N
查询	3	4	module_system:log:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	28	139	cab0cf25-f807-4d5b-be7a-142238495ccb	f	2026-06-21 18:12:31.023375	2026-06-21 18:12:31.023376	\N
登录日志删除	3	5	module_system:login_log:delete	\N	\N	\N	\N	\N	f	t	f	登录日志删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	28	140	8f2acc02-e88a-4eb1-80b5-2003eedb3b9c	f	2026-06-21 18:12:31.023378	2026-06-21 18:12:31.023378	\N
登录日志查询	3	6	module_system:login_log:query	\N	\N	\N	\N	\N	f	t	f	登录日志查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	28	141	9debaa35-d4ae-4fd3-a5da-ddcaa585bc6a	f	2026-06-21 18:12:31.023381	2026-06-21 18:12:31.023381	\N
新增	3	1	module_system:notice:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	29	142	d50b769f-13ea-4d11-9ae8-dc24014aecb4	f	2026-06-21 18:12:31.023384	2026-06-21 18:12:31.023384	\N
编辑	3	2	module_system:notice:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	29	143	089054cb-4a35-44e3-a8a7-7380763cf031	f	2026-06-21 18:12:31.023387	2026-06-21 18:12:31.023387	\N
删除	3	3	module_system:notice:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	29	144	fb316cb8-db0d-4305-a008-d148edca258b	f	2026-06-21 18:12:31.02339	2026-06-21 18:12:31.02339	\N
导出	3	4	module_system:notice:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	29	145	d703ac5d-87b7-4d19-9581-6e2da654f407	f	2026-06-21 18:12:31.023393	2026-06-21 18:12:31.023393	\N
状态变更	3	5	module_system:notice:patch	\N	\N	\N	\N	\N	f	t	f	状态变更	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	29	146	a55a4ac7-7ed1-4af6-93f3-89465001dc75	f	2026-06-21 18:12:31.023396	2026-06-21 18:12:31.023396	\N
详情	3	6	module_system:notice:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	29	147	b9a2448c-6b9f-4bb4-8bfe-7701adafa291	f	2026-06-21 18:12:31.023399	2026-06-21 18:12:31.023399	\N
查询	3	5	module_system:notice:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	29	148	1e9e0941-f612-4465-b587-34386d6168ae	f	2026-06-21 18:12:31.023402	2026-06-21 18:12:31.023402	\N
查询	3	1	module_system:ticket:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	30	149	aa990edc-82db-4d43-a5ee-5d16258cdb11	f	2026-06-21 18:12:31.023405	2026-06-21 18:12:31.023405	\N
新增	3	2	module_system:ticket:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	30	150	ecf33236-57e8-4d14-86fa-d57abea468c5	f	2026-06-21 18:12:31.023407	2026-06-21 18:12:31.023408	\N
编辑	3	3	module_system:ticket:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	30	151	14bf30ba-e0b0-4245-87be-d6812f418268	f	2026-06-21 18:12:31.02341	2026-06-21 18:12:31.023411	\N
删除	3	4	module_system:ticket:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	30	152	f585dcb8-c1e1-4765-ba3d-3ce6d38f0f56	f	2026-06-21 18:12:31.023413	2026-06-21 18:12:31.023413	\N
详情	3	5	module_system:ticket:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	30	153	4b5eb154-69da-4405-8c96-7f6ca517b5f8	f	2026-06-21 18:12:31.023416	2026-06-21 18:12:31.023416	\N
导出	3	6	module_system:ticket:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	30	154	a370c233-ae21-45ab-91cf-eb675610373f	f	2026-06-21 18:12:31.023419	2026-06-21 18:12:31.023419	\N
批量操作	3	7	module_system:ticket:patch	\N	\N	\N	\N	\N	f	t	f	批量操作	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	30	155	adf526d5-1503-4b16-ab47-81ae0b5a0a3c	f	2026-06-21 18:12:31.023422	2026-06-21 18:12:31.023422	\N
强制下线	3	1	module_monitor:online:delete	\N	\N	\N	\N	\N	f	t	f	强制下线	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	32	156	ce1d96a4-604d-4bb7-a519-dfcae1bf1307	f	2026-06-21 18:12:31.023425	2026-06-21 18:12:31.023425	\N
清除缓存	3	1	module_monitor:cache:delete	\N	\N	\N	\N	\N	f	t	f	清除缓存	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	34	157	37b01488-74f5-45b3-8328-18e52370ce07	f	2026-06-21 18:12:31.023427	2026-06-21 18:12:31.023428	\N
详情	3	2	module_monitor:cache:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	34	158	d47d1489-f053-44e0-8d2f-95f532e35fa1	f	2026-06-21 18:12:31.02343	2026-06-21 18:12:31.023431	\N
上传	3	1	module_monitor:resource:upload	\N	\N	\N	\N	\N	f	t	f	上传	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	35	159	07bd7143-7ab3-422d-bbf1-4f186c67f714	f	2026-06-21 18:12:31.023433	2026-06-21 18:12:31.023434	\N
下载	3	2	module_monitor:resource:download	\N	\N	\N	\N	\N	f	t	f	下载	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	35	160	95ee6ac9-f4cb-49d5-9350-7716562504ef	f	2026-06-21 18:12:31.023436	2026-06-21 18:12:31.023436	\N
删除	3	3	module_monitor:resource:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	35	161	6f1ef0f4-fa87-4a60-a23a-b498be2d6631	f	2026-06-21 18:12:31.023439	2026-06-21 18:12:31.023439	\N
移动	3	4	module_monitor:resource:move	\N	\N	\N	\N	\N	f	t	f	移动	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	35	162	979bb6e4-ff52-4c1a-900d-a3cf24b4030c	f	2026-06-21 18:12:31.023442	2026-06-21 18:12:31.023442	\N
复制	3	5	module_monitor:resource:copy	\N	\N	\N	\N	\N	f	t	f	复制	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	35	163	72033c8f-e8fe-4e10-b371-6b0e2b34a527	f	2026-06-21 18:12:31.023445	2026-06-21 18:12:31.023445	\N
重命名	3	6	module_monitor:resource:rename	\N	\N	\N	\N	\N	f	t	f	重命名	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	35	164	977aeb8e-e8e1-49d0-be65-e7743bb9476f	f	2026-06-21 18:12:31.023447	2026-06-21 18:12:31.023448	\N
新增	3	7	module_monitor:resource:create_dir	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	35	165	d2fa8209-07b7-481c-b0ed-e25851c05cd2	f	2026-06-21 18:12:31.02345	2026-06-21 18:12:31.023451	\N
导出	3	9	module_monitor:resource:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	platform	0	初始化数据	35	166	17af51f5-9685-4032-bf57-bb526ea43602	f	2026-06-21 18:12:31.023453	2026-06-21 18:12:31.023453	\N
查询	3	1	module_generator:gencode:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	platform	0	查询代码生成业务表列表	38	167	c0ffc4b7-89a6-4696-947d-70e722475bd5	f	2026-06-21 18:12:31.023456	2026-06-21 18:12:31.023456	\N
新增	3	2	module_generator:gencode:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	platform	0	创建表结构	38	168	57205d6e-d248-40f8-8915-efe0504cf8d0	f	2026-06-21 18:12:31.023459	2026-06-21 18:12:31.023459	\N
编辑	3	3	module_generator:gencode:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	platform	0	编辑业务表信息	38	169	e609ce97-56c7-46c6-906b-9340f9fa49d1	f	2026-06-21 18:12:31.023462	2026-06-21 18:12:31.023462	\N
删除	3	4	module_generator:gencode:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	platform	0	删除业务表信息	38	170	1a55aeca-5c4b-4c57-a66e-bf7355a69a78	f	2026-06-21 18:12:31.023464	2026-06-21 18:12:31.023465	\N
导入	3	5	module_generator:gencode:import	\N	\N	\N	\N	\N	f	t	f	导入	null	f	pc	\N	f	f	\N	f	\N	platform	0	导入表结构	38	171	5bad7f49-52bf-466a-9a9e-27b174ab81c0	f	2026-06-21 18:12:31.023467	2026-06-21 18:12:31.023468	\N
批量生成代码	3	6	module_generator:gencode:operate	\N	\N	\N	\N	\N	f	t	f	批量生成代码	null	f	pc	\N	f	f	\N	f	\N	platform	0	批量生成代码	38	172	13eb7e68-c98b-4f8a-96e6-e81f71ebf28f	f	2026-06-21 18:12:31.02347	2026-06-21 18:12:31.023471	\N
生成代码到指定路径	3	7	module_generator:gencode:code	\N	\N	\N	\N	\N	f	t	f	生成代码到指定路径	null	f	pc	\N	f	f	\N	f	\N	platform	0	生成代码到指定路径	38	173	9edb70f8-7193-415e-a90e-3f03b41b132a	f	2026-06-21 18:12:31.023473	2026-06-21 18:12:31.023474	\N
查询	3	8	module_generator:dblist:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	platform	0	查询数据库表列表	38	174	9c137521-10f9-4c98-bf8c-9483938aa465	f	2026-06-21 18:12:31.023476	2026-06-21 18:12:31.023476	\N
同步数据库	3	9	module_generator:db:sync	\N	\N	\N	\N	\N	f	t	f	同步数据库	null	f	pc	\N	f	f	\N	f	\N	platform	0	同步数据库	38	175	5d1ba607-bce2-45e5-966f-1694aef93b01	f	2026-06-21 18:12:31.023479	2026-06-21 18:12:31.023479	\N
AI对话	3	1	module_ai:chat:ws	\N	\N	\N	\N	\N	f	t	f	AI对话	null	f	pc	\N	f	f	\N	f	\N	platform	0	AI对话	39	176	1554c375-e21e-4cd4-98ea-55cc173ab276	f	2026-06-21 18:12:31.023482	2026-06-21 18:12:31.023482	\N
查询	3	2	module_ai:chat:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	platform	0	查询会话	39	177	e3eadcd9-168d-4a55-bd80-4cf401150500	f	2026-06-21 18:12:31.023485	2026-06-21 18:12:31.023485	\N
详情	3	3	module_ai:chat:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	platform	0	会话详情	39	178	2e3f5769-ae9e-4384-872c-a4b2c4fdc26c	f	2026-06-21 18:12:31.023488	2026-06-21 18:12:31.023488	\N
新增	3	4	module_ai:chat:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	platform	0	创建会话	39	179	39ce9e66-ab0d-4349-9d4f-7848312a9ef9	f	2026-06-21 18:12:31.02349	2026-06-21 18:12:31.023491	\N
编辑	3	5	module_ai:chat:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	platform	0	更新会话	39	180	c161d4be-0780-4e20-833b-15be027152c6	f	2026-06-21 18:12:31.023493	2026-06-21 18:12:31.023494	\N
删除	3	6	module_ai:chat:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	platform	0	删除会话	39	181	7dc265d8-4044-4b46-a015-f5faf0dbda87	f	2026-06-21 18:12:31.023496	2026-06-21 18:12:31.023496	\N
查询	3	1	module_ai:chat:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	platform	0	查询会话记忆	40	182	f38b3b84-bec4-4da8-baa1-a8cd6874135c	f	2026-06-21 18:12:31.023499	2026-06-21 18:12:31.023499	\N
详情	3	2	module_ai:chat:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	platform	0	会话记忆详情	40	183	aa6e724d-4930-40d8-9bb0-d22b3aad820b	f	2026-06-21 18:12:31.023502	2026-06-21 18:12:31.023502	\N
删除	3	3	module_ai:chat:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	platform	0	删除会话记忆	40	184	01c20dfe-4e3c-4223-bcdd-d85132f76515	f	2026-06-21 18:12:31.023505	2026-06-21 18:12:31.023505	\N
调度器监控	2	1	module_task:cronjob:job:query	ri:line-chart-line	Job	job	module_task/cronjob/job/index	\N	f	t	f	调度器监控	null	f	pc	\N	f	f	\N	f	\N	platform	0	调度器监控	41	185	d089ba94-34c8-469f-9b81-d138c956c170	f	2026-06-21 18:12:31.023507	2026-06-21 18:12:31.023508	\N
节点管理	2	2	module_task:cronjob:node:query	ri:mail-send-line	Node	node	module_task/cronjob/node/index	\N	f	t	f	节点管理	null	f	pc	\N	f	f	\N	f	\N	platform	0	节点管理	41	186	8accf4eb-5e89-4dc2-ab1b-7d015dfebb4e	f	2026-06-21 18:12:31.02351	2026-06-21 18:12:31.023511	\N
流程编排	2	1	module_task:workflow:definition:query	ri:tools-line	Workflow	task/workflow/definition	module_task/workflow/definition/index	\N	f	t	f	流程编排	null	f	pc	\N	f	f	\N	f	\N	platform	0	Vue Flow 画布与发布执行	42	187	5112502c-84fa-4123-9f25-379ae3bb56e1	f	2026-06-21 18:12:31.023513	2026-06-21 18:12:31.023514	\N
编排节点类型	2	2	module_task:workflow:node-type:query	ri:layout-grid-line	WorkflowNodeType	task/workflow/node-type	module_task/workflow/node-type/index	\N	f	t	f	编排节点类型	null	f	pc	\N	f	f	\N	f	\N	platform	0	画布节点类型与 Prefect 执行逻辑	42	188	27c0c761-8746-43ea-a86c-c63e89034914	f	2026-06-21 18:12:31.023516	2026-06-21 18:12:31.023517	\N
demo示例	2	1	module_example:demo:query	ri:menu-line	Demo	demo	module_example/demo/index	\N	f	t	f	demo示例	null	f	pc	\N	f	f	\N	f	\N	tenant	0	demo示例	43	189	0e79575f-54ce-4c37-9410-d9b4eb4613f2	f	2026-06-21 18:12:31.023519	2026-06-21 18:12:31.023519	\N
查询调度器	3	1	module_task:cronjob:job:query	\N	\N	\N	\N	\N	f	t	f	查询调度器	null	f	pc	\N	f	f	\N	f	\N	platform	0	查询调度器	185	190	300a3706-8479-411b-9ed2-e64b8139ec3b	f	2026-06-21 18:12:31.037907	2026-06-21 18:12:31.037911	\N
控制调度器	3	2	module_task:cronjob:job:scheduler	\N	\N	\N	\N	\N	f	t	f	控制调度器	null	f	pc	\N	f	f	\N	f	\N	platform	0	控制调度器	185	191	0c156686-7bf7-4780-820f-6385720cc949	f	2026-06-21 18:12:31.037916	2026-06-21 18:12:31.037917	\N
操作任务	3	3	module_task:cronjob:job:task	\N	\N	\N	\N	\N	f	t	f	操作任务	null	f	pc	\N	f	f	\N	f	\N	platform	0	操作任务	185	192	a6fb5905-68fc-4052-bef3-48e885a06e2e	f	2026-06-21 18:12:31.03792	2026-06-21 18:12:31.03792	\N
删除执行日志	3	4	module_task:cronjob:job:delete	\N	\N	\N	\N	\N	f	t	f	删除执行日志	null	f	pc	\N	f	f	\N	f	\N	platform	0	删除执行日志	185	193	440e5c39-c60b-44c1-8939-a2f730302f83	f	2026-06-21 18:12:31.037923	2026-06-21 18:12:31.037923	\N
详情执行日志	3	5	module_task:cronjob:job:detail	\N	\N	\N	\N	\N	f	t	f	详情执行日志	null	f	pc	\N	f	f	\N	f	\N	platform	0	详情执行日志	185	194	5a1bfb1c-4c74-4300-bca5-436452f2e7b2	f	2026-06-21 18:12:31.037926	2026-06-21 18:12:31.037926	\N
创建节点	3	1	module_task:cronjob:node:create	\N	\N	\N	\N	\N	f	t	f	创建节点	null	f	pc	\N	f	f	\N	f	\N	platform	0	创建节点	186	195	1337ea6e-4f6c-4ce6-932a-40a1f042742b	f	2026-06-21 18:12:31.037929	2026-06-21 18:12:31.037929	\N
调试节点	3	2	module_task:cronjob:node:execute	\N	\N	\N	\N	\N	f	t	f	调试节点	null	f	pc	\N	f	f	\N	f	\N	platform	0	调试节点	186	196	45a067b9-b7f1-4c38-b8a8-f98fa15b0912	f	2026-06-21 18:12:31.037932	2026-06-21 18:12:31.037932	\N
修改节点	3	3	module_task:cronjob:node:update	\N	\N	\N	\N	\N	f	t	f	修改节点	null	f	pc	\N	f	f	\N	f	\N	platform	0	修改节点	186	197	af048ec3-b45e-477f-935e-d6389de70d86	f	2026-06-21 18:12:31.037935	2026-06-21 18:12:31.037935	\N
删除节点	3	4	module_task:cronjob:node:delete	\N	\N	\N	\N	\N	f	t	f	删除节点	null	f	pc	\N	f	f	\N	f	\N	platform	0	删除节点	186	198	ae5a7b1e-922f-4c4c-ac38-c9c884e243a9	f	2026-06-21 18:12:31.037938	2026-06-21 18:12:31.037938	\N
详情节点	3	5	module_task:cronjob:node:detail	\N	\N	\N	\N	\N	f	t	f	详情节点	null	f	pc	\N	f	f	\N	f	\N	platform	0	详情节点	186	199	b8fdb120-8070-4de3-90d6-9a9812a6533c	f	2026-06-21 18:12:31.037941	2026-06-21 18:12:31.037942	\N
查询节点	3	6	module_task:cronjob:node:query	\N	\N	\N	\N	\N	f	t	f	查询节点	null	f	pc	\N	f	f	\N	f	\N	platform	0	查询节点	186	200	422ef761-c361-4555-98e1-c30ea48e767d	f	2026-06-21 18:12:31.037945	2026-06-21 18:12:31.037945	\N
创建流程	3	1	module_task:workflow:definition:create	\N	\N	\N	\N	\N	f	t	f	创建流程	null	f	pc	\N	f	f	\N	f	\N	platform	0	创建流程	187	201	8270c882-78f4-4332-875d-8ecaa262ce60	f	2026-06-21 18:12:31.037948	2026-06-21 18:12:31.037949	\N
执行流程	3	2	module_task:workflow:definition:execute	\N	\N	\N	\N	\N	f	t	f	执行流程	null	f	pc	\N	f	f	\N	f	\N	platform	0	执行流程	187	202	abcda894-fcfb-4094-b418-1815420c5a82	f	2026-06-21 18:12:31.037951	2026-06-21 18:12:31.037951	\N
修改流程	3	3	module_task:workflow:definition:update	\N	\N	\N	\N	\N	f	t	f	修改流程	null	f	pc	\N	f	f	\N	f	\N	platform	0	修改流程	187	203	78ee1aa7-5a41-4bb5-b1e0-bb8496daa62e	f	2026-06-21 18:12:31.037954	2026-06-21 18:12:31.037954	\N
删除流程	3	4	module_task:workflow:definition:delete	\N	\N	\N	\N	\N	f	t	f	删除流程	null	f	pc	\N	f	f	\N	f	\N	platform	0	删除流程	187	204	60fd27ae-5844-44f6-82df-4568470adb3f	f	2026-06-21 18:12:31.037957	2026-06-21 18:12:31.037957	\N
详情流程	3	5	module_task:workflow:definition:detail	\N	\N	\N	\N	\N	f	t	f	详情流程	null	f	pc	\N	f	f	\N	f	\N	platform	0	详情流程	187	205	3fa74930-9c25-468d-a031-38eacac855b1	f	2026-06-21 18:12:31.03796	2026-06-21 18:12:31.03796	\N
查询流程	3	6	module_task:workflow:definition:query	\N	\N	\N	\N	\N	f	t	f	查询流程	null	f	pc	\N	f	f	\N	f	\N	platform	0	查询流程	187	206	1e7afa54-f56f-411b-b928-2fc464f54778	f	2026-06-21 18:12:31.037963	2026-06-21 18:12:31.037963	\N
创建编排节点类型	3	1	module_task:workflow:node-type:create	\N	\N	\N	\N	\N	f	t	f	创建编排节点类型	null	f	pc	\N	f	f	\N	f	\N	platform	0	创建编排节点类型	188	207	b1dd60db-a2d8-43dd-b53a-4e3be50bffc9	f	2026-06-21 18:12:31.037966	2026-06-21 18:12:31.037966	\N
修改编排节点类型	3	2	module_task:workflow:node-type:update	\N	\N	\N	\N	\N	f	t	f	修改编排节点类型	null	f	pc	\N	f	f	\N	f	\N	platform	0	修改编排节点类型	188	208	95660a0f-e815-4f8a-95b7-678ad7ae6f09	f	2026-06-21 18:12:31.037969	2026-06-21 18:12:31.037969	\N
删除编排节点类型	3	3	module_task:workflow:node-type:delete	\N	\N	\N	\N	\N	f	t	f	删除编排节点类型	null	f	pc	\N	f	f	\N	f	\N	platform	0	删除编排节点类型	188	209	bfbaece2-d9c7-448b-b9b4-b890c53cafd4	f	2026-06-21 18:12:31.037971	2026-06-21 18:12:31.037972	\N
详情编排节点类型	3	4	module_task:workflow:node-type:detail	\N	\N	\N	\N	\N	f	t	f	详情编排节点类型	null	f	pc	\N	f	f	\N	f	\N	platform	0	详情编排节点类型	188	210	a75a3344-9b47-4a3b-a097-106877d2ab80	f	2026-06-21 18:12:31.037974	2026-06-21 18:12:31.037975	\N
查询编排节点类型	3	5	module_task:workflow:node-type:query	\N	\N	\N	\N	\N	f	t	f	查询编排节点类型	null	f	pc	\N	f	f	\N	f	\N	platform	0	查询编排节点类型	188	211	0808514e-c869-4bb9-9718-34ba0db999ac	f	2026-06-21 18:12:31.037977	2026-06-21 18:12:31.037978	\N
新增	3	1	module_example:demo:create	\N	\N	\N	\N	\N	f	t	f	新增	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	189	212	9714d0f1-1999-4b9d-a0a6-127f06553903	f	2026-06-21 18:12:31.03798	2026-06-21 18:12:31.037981	\N
编辑	3	2	module_example:demo:update	\N	\N	\N	\N	\N	f	t	f	编辑	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	189	213	e6de2cdd-a6e0-4c27-84e1-6684f0879ded	f	2026-06-21 18:12:31.037983	2026-06-21 18:12:31.037984	\N
删除	3	3	module_example:demo:delete	\N	\N	\N	\N	\N	f	t	f	删除	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	189	214	5e95f754-81a6-4e04-b744-ce6c3a5f1d5f	f	2026-06-21 18:12:31.037986	2026-06-21 18:12:31.037986	\N
状态变更	3	4	module_example:demo:patch	\N	\N	\N	\N	\N	f	t	f	状态变更	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	189	215	3adfea95-1365-4a37-8c5b-a4f359ac11fd	f	2026-06-21 18:12:31.037989	2026-06-21 18:12:31.037989	\N
导出	3	5	module_example:demo:export	\N	\N	\N	\N	\N	f	t	f	导出	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	189	216	9d8b4024-c39d-4855-9b96-f3fee10bb9b6	f	2026-06-21 18:12:31.037992	2026-06-21 18:12:31.037992	\N
导入	3	6	module_example:demo:import	\N	\N	\N	\N	\N	f	t	f	导入	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	189	217	7a5d6b79-e32a-43a5-b65b-c54b76f64c9a	f	2026-06-21 18:12:31.037995	2026-06-21 18:12:31.037995	\N
下载导入模板	3	7	module_example:demo:download	\N	\N	\N	\N	\N	f	t	f	下载导入模板	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	189	218	b67eb639-3436-415b-882b-2b99406084b1	f	2026-06-21 18:12:31.037998	2026-06-21 18:12:31.037998	\N
详情	3	8	module_example:demo:detail	\N	\N	\N	\N	\N	f	t	f	详情	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	189	219	c0d3a7d2-ff52-4dd9-9bba-2e296cfa4044	f	2026-06-21 18:12:31.038	2026-06-21 18:12:31.038001	\N
查询	3	9	module_example:demo:query	\N	\N	\N	\N	\N	f	t	f	查询	null	f	pc	\N	f	f	\N	f	\N	tenant	0	初始化数据	189	220	0abc3bcb-1de1-4af9-8749-334a2eb49f6f	f	2026-06-21 18:12:31.038003	2026-06-21 18:12:31.038004	\N
\.


--
-- Data for Name: platform_order; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_order (order_no, package_id, plugin_id, order_type, amount, period_count, pay_method, pay_time, expire_time, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id) FROM stdin;
202601010000001	2	\N	new	29900	12	alipay	2026-01-01 10:30:00	2026-01-01 10:45:00	1	星辰科技-标准版年付新购	1	d1cecb4b-0cb2-4dc5-9f32-cc76a623a5d0	f	2026-06-21 18:12:31.139521	2026-06-21 18:12:31.139525	\N	3
202603150000001	\N	2	plugin	9900	1	wxpay	2026-03-15 14:20:00	2026-03-15 14:35:00	1	星辰科技-AI助手插件购买	2	75eb0bc0-65f8-4ade-82ef-3b0e9b21c9e9	f	2026-06-21 18:12:31.13953	2026-06-21 18:12:31.13953	\N	3
202604010000001	4	\N	upgrade	269900	12	alipay	2026-04-01 09:00:00	2026-04-01 09:15:00	1	星辰科技-标准版升级为企业版	3	9b7b05b4-ecf6-4523-9bd6-0c02a32db9e1	f	2026-06-21 18:12:31.139534	2026-06-21 18:12:31.139534	\N	3
202602010000001	3	\N	new	99900	6	wxpay	2026-02-01 11:00:00	2026-02-01 11:15:00	3	创新工坊-专业版半年（已退款）	4	7848cfc9-5e24-4a42-b037-80bfaff4ed8a	f	2026-06-21 18:12:31.139537	2026-06-21 18:12:31.139538	\N	4
202605150000001	\N	4	plugin	19900	1	\N	\N	2026-05-15 16:45:00	2	创新工坊-工作流引擎（已取消）	5	f86331cd-71c7-4367-9661-72192306440f	f	2026-06-21 18:12:31.139541	2026-06-21 18:12:31.139541	\N	4
202606010000001	2	\N	new	29900	1	alipay	2026-06-01 08:30:00	2026-06-01 08:45:00	1	创新工坊-标准版月付新购	6	fa30e2fe-d65b-4432-9dc4-352e21ceed19	f	2026-06-21 18:12:31.139544	2026-06-21 18:12:31.139544	\N	4
202606100000001	\N	5	plugin	4900	1	wxpay	2026-06-10 15:00:00	2026-06-10 15:15:00	1	创新工坊-数据大屏插件购买	7	5f178daf-9190-4fc6-a04c-1c6c97e61159	f	2026-06-21 18:12:31.139547	2026-06-21 18:12:31.139547	\N	4
202606120000001	2	\N	renew	269100	12	alipay	2026-06-12 10:00:00	2026-06-12 10:15:00	1	星辰科技-企业版年付续费	8	3f4324c9-5253-4128-9ea4-92ef6bddafca	f	2026-06-21 18:12:31.13955	2026-06-21 18:12:31.13955	\N	3
202606120000002	\N	\N	new	0	0	\N	\N	2026-06-13 00:00:00	0	平台租户-测试待支付订单	9	b8df5394-e8f9-441f-929c-32a1830a449e	f	2026-06-21 18:12:31.139553	2026-06-21 18:12:31.139553	\N	1
\.


--
-- Data for Name: platform_package; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_package (name, code, sort, price, period, trial_days, max_users, max_roles, max_depts, max_storage_mb, rate_limit, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time) FROM stdin;
基础版	basic	1	0	month	7	10	5	10	1024	30	0	适合个人和小团队使用	1	a8e832c8-86fd-4817-b68b-dfc4b78d36c3	f	2026-06-21 18:12:30.968882	2026-06-21 18:12:30.968891	\N
标准版	standard	2	29900	month	0	50	20	50	10240	60	0	适合成长型企业	2	250c0a2e-2502-41fd-af8d-58b1c13ecf4b	f	2026-06-21 18:12:30.968897	2026-06-21 18:12:30.968898	\N
专业版	pro	3	99900	month	0	200	50	200	102400	120	0	适合中型企业	3	c0feb12a-3903-4a8f-a4ea-a455a11ac072	f	2026-06-21 18:12:30.968901	2026-06-21 18:12:30.968902	\N
企业版	enterprise	4	299900	year	0	1000	200	1000	1024000	300	0	适合大型企业和组织	4	80fb5577-d2f2-417b-9bfc-894f5a9a3fa4	f	2026-06-21 18:12:30.968905	2026-06-21 18:12:30.968905	\N
\.


--
-- Data for Name: platform_package_menu; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_package_menu (id, package_id, menu_id) FROM stdin;
1	1	7
2	1	8
3	1	9
4	1	10
5	2	2
6	2	5
7	2	6
8	2	7
9	2	8
10	2	9
11	2	10
12	3	1
13	3	2
14	3	3
15	3	5
16	3	6
17	3	7
18	3	8
19	3	9
20	3	10
21	4	1
22	4	2
23	4	3
24	4	4
25	4	5
26	4	6
27	4	7
28	4	8
29	4	9
30	4	10
\.


--
-- Data for Name: platform_package_plugin; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_package_plugin (id, package_id, plugin_id) FROM stdin;
\.


--
-- Data for Name: platform_payment_record; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_payment_record (order_id, transaction_id, pay_method, amount, raw_response, pay_time, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id) FROM stdin;
1	ALIP20260101000001	alipay	29900	\N	2026-01-01 10:30:00	1	星辰科技-标准版年付	1	c00326e6-e707-4a15-8c0b-5af1125e4956	f	2026-06-21 18:12:31.160946	2026-06-21 18:12:31.160948	\N	3
2	WXPAY202603150001	wxpay	9900	\N	2026-03-15 14:20:00	1	星辰科技-AI助手	2	a3f5daea-41c2-4234-a0da-3ebebe974062	f	2026-06-21 18:12:31.160952	2026-06-21 18:12:31.160953	\N	3
3	ALIP20260401000001	alipay	269900	\N	2026-04-01 09:00:00	1	星辰科技-升级企业版	3	d1f09c73-8287-458b-a469-0eaf6cc5fdde	f	2026-06-21 18:12:31.160956	2026-06-21 18:12:31.160956	\N	3
4	WXPAY202602010001	wxpay	99900	\N	2026-02-01 11:00:00	2	创新工坊-专业版半年（已退款）	4	82c9d965-8b32-427f-be48-010fefcb7887	f	2026-06-21 18:12:31.160959	2026-06-21 18:12:31.160959	\N	4
6	ALIP20260601000001	alipay	29900	\N	2026-06-01 08:30:00	1	创新工坊-标准版月付	5	bae67870-968e-4f41-a7d0-c30698876d3d	f	2026-06-21 18:12:31.160962	2026-06-21 18:12:31.160962	\N	4
7	WXPAY202606100001	wxpay	4900	\N	2026-06-10 15:00:00	1	创新工坊-数据大屏	6	f9527683-7bef-4359-8b01-be2f311819a2	f	2026-06-21 18:12:31.160965	2026-06-21 18:12:31.160966	\N	4
8	ALIP20260612000001	alipay	269100	\N	2026-06-12 10:00:00	1	星辰科技-企业版续费	7	2ac42316-b606-4dab-aab9-5c6926ddb434	f	2026-06-21 18:12:31.160968	2026-06-21 18:12:31.160969	\N	3
\.


--
-- Data for Name: platform_plugin; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_plugin (name, code, version, author, icon, category, price, menu_path, permission_prefix, dependencies, sort, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time) FROM stdin;
代码生成器	code_generator	1.0.0	FastApiAdmin	https://service.fastapiadmin.com/api/v1/static/image/plugin/code.png	tool	0	/tool/generator	tool:generator	\N	1	0	自动生成CRUD代码，支持多种模板	1	cded08a1-8261-465e-a7fd-9bd64b8df008	f	2026-06-21 18:12:30.987908	2026-06-21 18:12:30.987911	\N
AI助手	ai_assistant	1.0.0	FastApiAdmin	https://service.fastapiadmin.com/api/v1/static/image/plugin/ai.png	ai	9900	/ai/assistant	ai:assistant	\N	2	0	集成AI对话助手，支持智能问答	2	bda44433-46cc-4f2c-ba50-d257934b685c	f	2026-06-21 18:12:30.987916	2026-06-21 18:12:30.987916	\N
系统监控	system_monitor	1.0.0	FastApiAdmin	https://service.fastapiadmin.com/api/v1/static/image/plugin/monitor.png	monitor	0	/monitor/system	monitor:system	\N	3	0	实时监控系统运行状态，CPU、内存、磁盘等	3	0f07d96e-ea44-4f0d-b8b9-0997ee6d5854	f	2026-06-21 18:12:30.98792	2026-06-21 18:12:30.98792	\N
工作流引擎	workflow_engine	1.0.0	FastApiAdmin	https://service.fastapiadmin.com/api/v1/static/image/plugin/workflow.png	business	19900	/workflow/design	workflow:design	\N	4	0	可视化工作流设计器，支持审批流程	4	e93e8f89-c706-4ff4-8eb6-92ef9e270772	f	2026-06-21 18:12:30.987923	2026-06-21 18:12:30.987924	\N
数据大屏	data_dashboard	1.0.0	FastApiAdmin	https://service.fastapiadmin.com/api/v1/static/image/plugin/dashboard.png	business	4900	/dashboard/data	dashboard:data	\N	5	0	可视化数据大屏，支持多种图表	5	1a17b5c7-8460-4976-8a4b-ee567941e590	f	2026-06-21 18:12:30.987927	2026-06-21 18:12:30.987927	\N
\.


--
-- Data for Name: platform_refund; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_refund (order_id, refund_no, amount, reason, refund_transaction_id, reviewer_id, review_time, reject_reason, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id) FROM stdin;
4	RF20260220000001	99900	套餐选择错误，申请退款并更换为标准版	WXREFUND20260220001	2	2026-02-20 16:30:00	\N	2	创新工坊-专业版退款（已通过）	1	c5a8b581-b82c-4feb-82e2-2e73f547d753	f	2026-06-21 18:12:31.167713	2026-06-21 18:12:31.167716	\N	4
\.


--
-- Data for Name: platform_tenant; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_tenant (name, code, contact_name, contact_phone, contact_email, address, domain, logo_url, sort, package_id, start_time, end_time, version, favicon, login_bg, copyright, keep_record, help_doc, privacy, clause, git_code, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time) FROM stdin;
平台租户	system	管理员	13800138000	admin@fastapiadmin.com	陕西省西安市	\N	https://service.fastapiadmin.com/api/v1/static/image/logo.svg	0	\N	\N	\N	1.0.0	https://service.fastapiadmin.com/api/v1/static/image/favicon.ico	https://service.fastapiadmin.com/api/v1/static/image/background.svg	Copyright © 2025-2027 service.fastapiadmin.com 版权所有	陕ICP备2025069493号-1	https://docs.fastapiadmin.com	https://fastapiadmin.com/privacy	https://fastapiadmin.com/clause	https://github.com/fastapi-admin/fastapi-admin	0	平台默认租户，id 固定为 1，管理平台所有资源（不受套餐限制）	1	30480da4-1170-4cee-944a-001fbec711a4	f	2026-06-21 18:12:30.976436	2026-06-21 18:12:30.976439	\N
测试租户	test	测试管理员	13800138001	test@fastapiadmin.com	上海市浦东新区	test.fastapiadmin.com	https://service.fastapiadmin.com/api/v1/static/image/logo.png	1	2	2024-01-01 00:00:00	2027-12-31 23:59:59	1.0.0	https://service.fastapiadmin.com/api/v1/static/image/favicon.ico	https://service.fastapiadmin.com/api/v1/static/image/background.svg	Copyright © 2024 Test Tenant 版权所有	陕ICP备2024000000号	https://docs.fastapiadmin.com	https://fastapiadmin.com/privacy	https://fastapiadmin.com/clause	\N	0	测试租户，用于功能测试	2	22134109-46ba-40bd-b3d9-1b70d8b6e243	f	2026-06-21 18:12:30.976443	2026-06-21 18:12:30.976444	\N
星辰科技有限公司	STAR	张明	13800001001	zhang@star-tech.dev	\N	\N	\N	0	2	\N	\N	\N	\N	\N	2026 星辰科技	\N	\N	\N	\N	\N	0	中型科技企业，使用标准版套餐	3	d3afc62d-3091-42a9-bb71-64d02e4a02b5	f	2026-06-21 18:12:30.980574	2026-06-21 18:12:30.980579	\N
创新工坊	INNO	李芳	13800002001	li@inno.work	\N	\N	\N	0	1	\N	\N	\N	\N	\N	2026 创新工坊	\N	\N	\N	\N	\N	0	初创团队，使用基础版免费试用	4	7a1ddb29-a8d3-4103-91d1-af80bfb444c7	f	2026-06-21 18:12:30.980584	2026-06-21 18:12:30.980584	\N
\.


--
-- Data for Name: platform_tenant_plugin; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_tenant_plugin (id, tenant_id, plugin_id, enabled, purchased, installed_time) FROM stdin;
1	1	1	t	f	2024-01-01 00:00:00
2	1	2	t	f	2024-01-01 00:00:00
3	1	3	t	f	2024-01-01 00:00:00
4	1	4	t	f	2024-01-01 00:00:00
5	1	5	t	f	2024-01-01 00:00:00
6	2	1	t	f	2024-01-01 00:00:00
7	2	3	t	f	2024-01-01 00:00:00
8	2	5	t	f	2024-01-01 00:00:00
\.


--
-- Data for Name: platform_user_tenant; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.platform_user_tenant (id, user_id, tenant_id, role, is_default, create_time) FROM stdin;
1	1	1	owner	1	2026-06-21 18:12:31.177576
2	2	1	admin	1	2026-06-21 18:12:31.177579
3	3	1	member	1	2026-06-21 18:12:31.17758
4	4	1	member	1	2026-06-21 18:12:31.17758
5	5	1	member	1	2026-06-21 18:12:31.177581
6	1	3	owner	0	2026-06-21 18:12:31.177581
7	6	3	owner	1	2026-06-21 18:12:31.177581
8	7	3	member	1	2026-06-21 18:12:31.177582
9	8	4	owner	1	2026-06-21 18:12:31.177582
10	9	4	member	1	2026-06-21 18:12:31.177583
\.


--
-- Data for Name: sys_dept; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_dept (name, status, description, "order", code, leader, phone, email, parent_id, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
集团总公司	0	集团总部	1	GROUP	张总	13800138000	ceo@example.com	\N	1	8d491001-1576-4fba-b24f-426fac850a9c	f	2026-06-21 18:12:31.05792	2026-06-21 18:12:31.057931	\N	1	\N	\N	\N
星辰研发中心	0	星辰科技研发部门	1	STAR_RND	\N	\N	\N	\N	2	7074dea5-04f4-4d3c-bf86-56b941520286	f	2026-06-21 18:12:31.05794	2026-06-21 18:12:31.057941	\N	3	\N	\N	\N
星辰市场部	0	星辰科技市场部门	2	STAR_MKT	\N	\N	\N	\N	3	16390a1a-bf3b-412c-a010-d0c4eec97aee	f	2026-06-21 18:12:31.057949	2026-06-21 18:12:31.05795	\N	3	\N	\N	\N
创新产品部	0	创新工坊产品团队	1	INNO_PROD	\N	\N	\N	\N	4	67defd37-6f79-43b0-a8b0-854adb64000b	f	2026-06-21 18:12:31.057956	2026-06-21 18:12:31.057957	\N	4	\N	\N	\N
创新技术部	0	创新工坊技术团队	2	INNO_TECH	\N	\N	\N	\N	5	128f2d60-9a67-4b1d-a204-30b65228a75e	f	2026-06-21 18:12:31.057963	2026-06-21 18:12:31.057964	\N	4	\N	\N	\N
技术研发部	0	负责技术研发	1	TECH	李工	13800138001	tech@example.com	1	6	6c3c2955-759d-4565-9110-244ef9c019dc	f	2026-06-21 18:12:31.061584	2026-06-21 18:12:31.061588	\N	1	\N	\N	\N
产品运营部	0	产品与运营	2	PRODUCT	赵经理	13800138004	product@example.com	1	7	4d846e41-f9ee-49dc-bba9-2329f559ea45	f	2026-06-21 18:12:31.061593	2026-06-21 18:12:31.061594	\N	1	\N	\N	\N
人力资源部	0	人事管理	3	HR	刘经理	13800138005	hr@example.com	1	8	4da4ab56-ff9a-40cd-98cd-e134541e04e7	f	2026-06-21 18:12:31.061598	2026-06-21 18:12:31.061599	\N	1	\N	\N	\N
前端组	0	\N	1	STAR_FE	\N	\N	\N	2	9	2bd7e45d-f95f-41d0-80ed-3bc0316d6239	f	2026-06-21 18:12:31.061602	2026-06-21 18:12:31.061603	\N	3	\N	\N	\N
后端组	0	\N	2	STAR_BE	\N	\N	\N	2	10	534e821d-5e37-47c5-9675-9531c74572cc	f	2026-06-21 18:12:31.061607	2026-06-21 18:12:31.061607	\N	3	\N	\N	\N
测试组	0	\N	3	STAR_QA	\N	\N	\N	2	11	705bdd34-c06c-4696-bb1c-d5996d230de4	f	2026-06-21 18:12:31.061611	2026-06-21 18:12:31.061611	\N	3	\N	\N	\N
后端开发组	0	后端技术开发	1	BACKEND	王工	13800138002	backend@example.com	6	12	f41c1a2d-f300-43b4-a76b-674f07aecfee	f	2026-06-21 18:12:31.066493	2026-06-21 18:12:31.066497	\N	1	\N	\N	\N
前端开发组	0	前端技术开发	2	FRONTEND	陈工	13800138003	frontend@example.com	6	13	73df2b76-36bc-4b7e-89ce-5dd91afb035c	f	2026-06-21 18:12:31.066502	2026-06-21 18:12:31.066502	\N	1	\N	\N	\N
\.


--
-- Data for Name: sys_dict_data; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_dict_data (status, description, dict_sort, dict_label, dict_value, css_class, list_class, is_default, dict_type, dict_type_id, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id) FROM stdin;
0	性别男	1	男	0	blue	\N	t	sys_user_sex	1	1	ca3b3c1c-70fe-4c20-b3fd-16043673ed56	f	2026-06-21 18:12:31.089835	2026-06-21 18:12:31.08984	\N	1
0	性别女	2	女	1	pink	\N	f	sys_user_sex	1	2	f792d845-0a26-4dae-8121-7c52446be83e	f	2026-06-21 18:12:31.089844	2026-06-21 18:12:31.089845	\N	1
0	性别未知	3	未知	2	red	\N	f	sys_user_sex	1	3	88984d03-bbc3-489b-bf05-7e1ea5b62145	f	2026-06-21 18:12:31.089848	2026-06-21 18:12:31.089848	\N	1
0	是	1	是	1		primary	t	sys_yes_no	2	4	e2ecb880-c769-4175-8419-c291c5cd99c1	f	2026-06-21 18:12:31.089851	2026-06-21 18:12:31.089851	\N	1
0	否	2	否	0		danger	f	sys_yes_no	2	5	340669ef-647c-4197-96ca-0e1a7ad2aee7	f	2026-06-21 18:12:31.089854	2026-06-21 18:12:31.089854	\N	1
0	启用状态	1	启用	1		primary	f	sys_common_status	3	6	29700ed7-293a-4663-8761-c5e7ea0e56ab	f	2026-06-21 18:12:31.089857	2026-06-21 18:12:31.089857	\N	1
0	停用状态	2	停用	0		danger	f	sys_common_status	3	7	f3e2eed8-bcd8-4de0-ba40-c25ca1a0b901	f	2026-06-21 18:12:31.08986	2026-06-21 18:12:31.08986	\N	1
0	通知	1	通知	1	blue	warning	t	sys_notice_type	4	8	8413627d-ce3f-4fec-8600-398f5aa61231	f	2026-06-21 18:12:31.089863	2026-06-21 18:12:31.089864	\N	1
0	公告	2	公告	2	orange	success	f	sys_notice_type	4	9	99b44a62-ec8a-4901-910b-27b24662c425	f	2026-06-21 18:12:31.089866	2026-06-21 18:12:31.089867	\N	1
0	其他操作	99	其他	0		info	f	sys_oper_type	5	10	d71f562d-1688-4a01-86b4-c6d3689eaad8	f	2026-06-21 18:12:31.089869	2026-06-21 18:12:31.08987	\N	1
0	新增操作	1	新增	1		info	f	sys_oper_type	5	11	56673ff2-34d9-43cc-ba20-07c5a629ccf4	f	2026-06-21 18:12:31.089872	2026-06-21 18:12:31.089873	\N	1
0	修改操作	2	修改	2		info	f	sys_oper_type	5	12	55ef31d3-b742-444c-8f96-cb1a7f5c15d1	f	2026-06-21 18:12:31.089875	2026-06-21 18:12:31.089876	\N	1
0	删除操作	3	删除	3		danger	f	sys_oper_type	5	13	2b0cda43-e042-4fe9-842a-5631f8e5c096	f	2026-06-21 18:12:31.089878	2026-06-21 18:12:31.089879	\N	1
0	授权操作	4	分配权限	4		primary	f	sys_oper_type	5	14	322bbf86-4618-4830-abf7-cad0da9b4f15	f	2026-06-21 18:12:31.089882	2026-06-21 18:12:31.089882	\N	1
0	导出操作	5	导出	5		warning	f	sys_oper_type	5	15	a333f8a0-0381-4c50-88f4-71c2618963b7	f	2026-06-21 18:12:31.089885	2026-06-21 18:12:31.089885	\N	1
0	导入操作	6	导入	6		warning	f	sys_oper_type	5	16	3818a7f3-ac7c-4b27-9029-d4234a2ca719	f	2026-06-21 18:12:31.089888	2026-06-21 18:12:31.089888	\N	1
0	强退操作	7	强退	7		danger	f	sys_oper_type	5	17	db743963-27b4-4600-bf8a-d7d310df61d0	f	2026-06-21 18:12:31.089891	2026-06-21 18:12:31.089891	\N	1
0	生成操作	8	生成代码	8		warning	f	sys_oper_type	5	18	3b4f7c80-22d9-4756-bdb4-e3bb790e8c0a	f	2026-06-21 18:12:31.089894	2026-06-21 18:12:31.089894	\N	1
0	清空操作	9	清空数据	9		danger	f	sys_oper_type	5	19	3547b03a-6272-4c49-b72b-bb41d43a8f75	f	2026-06-21 18:12:31.089897	2026-06-21 18:12:31.089897	\N	1
0	默认分组	1	默认(Memory)	default		\N	t	sys_job_store	6	20	9c902291-13af-4bcd-b636-d39a1afcddf6	f	2026-06-21 18:12:31.0899	2026-06-21 18:12:31.0899	\N	1
0	数据库分组	2	数据库(Sqlalchemy)	sqlalchemy		\N	f	sys_job_store	6	21	66d91458-82be-47ad-9af4-85d456df6f54	f	2026-06-21 18:12:31.089903	2026-06-21 18:12:31.089903	\N	1
0	reids分组	3	数据库(Redis)	redis		\N	f	sys_job_store	6	22	5dcacdb0-4076-43a3-9b5b-ce392e8ed193	f	2026-06-21 18:12:31.089906	2026-06-21 18:12:31.089906	\N	1
0	线程池	1	线程池	default		\N	f	sys_job_executor	7	23	64c542b2-934d-4c9c-961e-9942f778402f	f	2026-06-21 18:12:31.089909	2026-06-21 18:12:31.089909	\N	1
0	进程池	2	进程池	processpool		\N	f	sys_job_executor	7	24	644d40b1-5290-443f-998c-21c6742790cf	f	2026-06-21 18:12:31.089912	2026-06-21 18:12:31.089912	\N	1
0	演示函数	1	演示函数	scheduler_test.job		\N	t	sys_job_function	8	25	13993fb7-1ecf-43bf-b0a4-3b5560f8adde	f	2026-06-21 18:12:31.089915	2026-06-21 18:12:31.089915	\N	1
0	指定日期任务触发器	1	指定日期(date)	date		\N	t	sys_job_trigger	9	26	0729134f-e2b9-4948-8c39-8d8ea0160dcd	f	2026-06-21 18:12:31.089919	2026-06-21 18:12:31.089919	\N	1
0	间隔触发器任务触发器	2	间隔触发器(interval)	interval		\N	f	sys_job_trigger	9	27	cdf57cb4-de2f-4152-b2ba-4b5e16dde42d	f	2026-06-21 18:12:31.089922	2026-06-21 18:12:31.089922	\N	1
0	间隔触发器任务触发器	3	cron表达式	cron		\N	f	sys_job_trigger	9	28	f4264e8a-a3ab-413b-aa5d-49319a361e5d	f	2026-06-21 18:12:31.089925	2026-06-21 18:12:31.089925	\N	1
0	默认表格回显样式	1	默认(default)	default		\N	t	sys_list_class	10	29	96658393-0ee2-4727-9632-e69c84316356	f	2026-06-21 18:12:31.089928	2026-06-21 18:12:31.089928	\N	1
0	主要表格回显样式	2	主要(primary)	primary		\N	f	sys_list_class	10	30	be2ddcaf-a104-4f34-97d9-4666114c6671	f	2026-06-21 18:12:31.089931	2026-06-21 18:12:31.089931	\N	1
0	成功表格回显样式	3	成功(success)	success		\N	f	sys_list_class	10	31	d1de6b5e-ee4e-4e62-8cd9-453d485c5ebf	f	2026-06-21 18:12:31.089934	2026-06-21 18:12:31.089934	\N	1
0	信息表格回显样式	4	信息(info)	info		\N	f	sys_list_class	10	32	5b0fa3d7-5636-4edb-8b9a-4771cb7b4d97	f	2026-06-21 18:12:31.089937	2026-06-21 18:12:31.089937	\N	1
0	警告表格回显样式	5	警告(warning)	warning		\N	f	sys_list_class	10	33	20532bb1-9f32-4432-9b36-e44cc67accab	f	2026-06-21 18:12:31.08994	2026-06-21 18:12:31.08994	\N	1
0	危险表格回显样式	6	危险(danger)	danger		\N	f	sys_list_class	10	34	f09ac803-ecec-40cb-bba1-dafd1a392d8b	f	2026-06-21 18:12:31.089943	2026-06-21 18:12:31.089943	\N	1
\.


--
-- Data for Name: sys_dict_type; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_dict_type (dict_name, dict_type, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id) FROM stdin;
用户性别	sys_user_sex	0	用户性别列表	1	61c77fc8-a4fa-468e-8908-716715e11f95	f	2026-06-21 18:12:31.079114	2026-06-21 18:12:31.079116	\N	1
系统是否	sys_yes_no	0	系统是否列表	2	0609d6e7-0940-4006-97e6-0c1b212f11c2	f	2026-06-21 18:12:31.07912	2026-06-21 18:12:31.07912	\N	1
系统状态	sys_common_status	0	系统状态	3	fe7c6924-ab4c-43cd-a8c1-297083298b96	f	2026-06-21 18:12:31.079124	2026-06-21 18:12:31.079124	\N	1
通知类型	sys_notice_type	0	通知类型列表	4	95227e49-dab5-4050-96b1-34a0e07beef7	f	2026-06-21 18:12:31.079127	2026-06-21 18:12:31.079127	\N	1
操作类型	sys_oper_type	0	操作类型列表	5	78f68ac8-99e5-469c-9562-18049711ac1a	f	2026-06-21 18:12:31.07913	2026-06-21 18:12:31.07913	\N	1
任务存储器	sys_job_store	0	任务分组列表	6	561d2d1d-4ea7-4a58-b28e-22c2f4e1b92b	f	2026-06-21 18:12:31.079133	2026-06-21 18:12:31.079133	\N	1
任务执行器	sys_job_executor	0	任务执行器列表	7	193fb375-3f6f-446d-878e-2759b91320ab	f	2026-06-21 18:12:31.079136	2026-06-21 18:12:31.079136	\N	1
任务函数	sys_job_function	0	任务函数列表	8	4d967142-73de-4ff7-9c31-52fae467b625	f	2026-06-21 18:12:31.079139	2026-06-21 18:12:31.079139	\N	1
任务触发器	sys_job_trigger	0	任务触发器列表	9	85a1c85f-8d0f-4a0a-a81e-5a63e401b1fc	f	2026-06-21 18:12:31.079142	2026-06-21 18:12:31.079142	\N	1
表格回显样式	sys_list_class	0	表格回显样式列表	10	67c9bf20-504e-4908-b02c-90d461d12621	f	2026-06-21 18:12:31.079145	2026-06-21 18:12:31.079145	\N	1
\.


--
-- Data for Name: sys_login_log; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_login_log (status, description, username, login_location, login_ip, request_os, request_browser, msg, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
1	\N	super	陕西省西安市	127.0.0.1	macOS 14.5	Chrome 125	登录成功	1	d1031c26-b1cf-4a31-994f-5b4cee5bd472	f	2026-06-21 18:12:31.219726	2026-06-21 18:12:31.219728	\N	1	\N	\N	\N
1	\N	admin	陕西省西安市	127.0.0.1	macOS 14.5	Chrome 125	登录成功	2	9e154fe0-0d77-40cb-a22f-f37d0171dcbd	f	2026-06-21 18:12:31.219732	2026-06-21 18:12:31.219733	\N	1	\N	\N	\N
1	\N	user	北京市	192.168.1.100	Windows 11	Edge 125	登录成功	3	67e6e39b-97a7-47bc-9ac0-cd6dec19095c	f	2026-06-21 18:12:31.219736	2026-06-21 18:12:31.219736	\N	1	\N	\N	\N
2	\N	super	广东省深圳市	203.0.113.50	Unknown	Unknown	密码错误，剩余尝试次数: 4	4	ba84de33-6419-4343-ba7a-29a7b892fbad	f	2026-06-21 18:12:31.219739	2026-06-21 18:12:31.219739	\N	1	\N	\N	\N
1	\N	product	上海市	10.0.0.88	macOS 14.6	Safari 17.5	登录成功	5	0a0ed73d-4331-4e54-825e-9979aecc3b76	f	2026-06-21 18:12:31.219742	2026-06-21 18:12:31.219743	\N	1	\N	\N	\N
1	\N	zhang_admin	浙江省杭州市	172.16.0.10	Windows 10	Chrome 124	登录成功	6	9680de53-b0ae-4167-b0ee-f85a7a2d3a7a	f	2026-06-21 18:12:31.219745	2026-06-21 18:12:31.219746	\N	3	\N	\N	\N
1	\N	wang_dev	浙江省杭州市	172.16.0.20	Ubuntu 22.04	Firefox 126	登录成功	7	ba8b5ce6-173a-44e5-a477-dff4b23e9110	f	2026-06-21 18:12:31.219748	2026-06-21 18:12:31.219749	\N	3	\N	\N	\N
1	\N	li_admin	四川省成都市	10.10.10.5	macOS 15.0	Chrome 126	登录成功	8	732e2da9-8f13-4392-873b-9b75a575ab4b	f	2026-06-21 18:12:31.219751	2026-06-21 18:12:31.219752	\N	4	\N	\N	\N
1	\N	zhao_eng	四川省成都市	10.10.10.6	macOS 15.0	Chrome 126	登录成功	9	5359acf8-bf4d-4cf0-a937-f1b1b54115ee	f	2026-06-21 18:12:31.219754	2026-06-21 18:12:31.219755	\N	4	\N	\N	\N
2	\N	hr	陕西省西安市	127.0.0.1	Windows 11	Chrome 125	账号已被锁定，请15分钟后重试	10	a792c568-46ac-42cf-ae88-6a14cb6186f8	f	2026-06-21 18:12:31.219757	2026-06-21 18:12:31.219758	\N	1	\N	\N	\N
1	\N	super	日本东京	203.104.209.5	iOS 18.0	Safari Mobile	登录成功	11	3a732055-41c8-480a-bdb5-3a005cad734c	f	2026-06-21 18:12:31.21976	2026-06-21 18:12:31.21976	\N	1	\N	\N	\N
2	\N	test_user	美国洛杉矶	198.51.100.1	Unknown	Unknown	用户不存在	12	39a1825d-0fe1-463b-b31e-157226f69ab3	f	2026-06-21 18:12:31.219763	2026-06-21 18:12:31.219763	\N	1	\N	\N	\N
\.


--
-- Data for Name: sys_notice; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_notice (notice_title, notice_type, notice_content, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
系统上线公告	2	<p>欢迎使用 FastApiAdmin 系统！</p><p>这是一个功能强大的权限管理系统，支持多租户、角色权限控制等功能。</p>	0	系统上线公告	1	3636ecdb-10ec-4c4e-a354-0f1b426483bb	f	2026-06-21 18:12:31.198024	2026-06-21 18:12:31.198029	\N	1	\N	\N	\N
系统维护通知	1	<p>系统将于本周六凌晨2:00-4:00进行例行维护，请提前保存工作。</p>	0	系统维护通知	2	07a08a92-499b-44a8-ab44-d547e9f0879a	f	2026-06-21 18:12:31.198037	2026-06-21 18:12:31.198037	\N	1	\N	\N	\N
新功能发布	2	<p>本次更新新增了工作流引擎、代码生成器等功能，欢迎体验！</p>	0	新功能发布	3	d5632105-3082-4031-85be-d4b266720bbc	f	2026-06-21 18:12:31.198041	2026-06-21 18:12:31.198041	\N	1	\N	\N	\N
安全更新提醒	1	<p>请所有用户尽快更新密码，建议使用至少8位包含大小写字母、数字和特殊字符的强密码。</p><p>更新方法：登录后进入「个人中心」->「修改密码」。</p>	0	安全更新提醒	4	8cc439e6-2fcf-4d9e-b9b9-20120828e48c	f	2026-06-21 18:12:31.198044	2026-06-21 18:12:31.198044	\N	1	\N	\N	\N
节假日值班安排	1	<p>春节假期（2月10日-2月17日）期间系统值班安排如下：</p><p>联系电话：138-0000-0000</p><p>紧急问题请直接联系值班人员。</p>	0	节假日值班通知	5	73581409-62b1-4987-9909-4c3e09502ba5	f	2026-06-21 18:12:31.198047	2026-06-21 18:12:31.198047	\N	1	\N	\N	\N
v2.0 版本升级公告	2	<p>v2.0 大版本即将发布，主要更新：</p><ul><li>全新工作流引擎</li><li>AI助手集成</li><li>代码生成器增强</li><li>性能优化 30%</li></ul><p>升级时间另行通知。</p>	0	v2.0 版本升级公告	6	148966e0-a69f-4afa-b79e-1f0c142ead51	f	2026-06-21 18:12:31.19805	2026-06-21 18:12:31.19805	\N	1	\N	\N	\N
\.


--
-- Data for Name: sys_notice_read; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_notice_read (user_id, notice_id, read_time) FROM stdin;
1	1	2025-06-01 09:15:00
1	2	2025-06-10 08:30:00
1	3	2025-07-01 10:00:00
2	1	2025-06-01 09:20:00
2	2	2025-06-10 09:00:00
3	1	2025-06-01 10:30:00
4	1	2025-06-02 14:00:00
5	1	2025-06-03 11:00:00
6	6	2025-06-20 10:00:00
8	2	2025-06-10 16:00:00
\.


--
-- Data for Name: sys_operation_log; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_operation_log (status, description, request_path, request_method, request_payload, response_code, response_json, process_time, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
0	用户登录	/api/v1/system/auth/login	POST	{"username": "super", "password": "***"}	200	{"code": 200, "msg": "登录成功"}	45ms	1	4ec1c829-c9ee-4128-b14b-9dbbd626357e	f	2026-06-21 18:12:31.229524	2026-06-21 18:12:31.229527	\N	1	\N	\N	\N
0	获取当前用户信息	/api/v1/system/user/current/info	GET	\N	200	{"code": 200, "data": {"username": "super"}}	12ms	2	1f3492a9-58f7-49ab-bdcf-ce7e412cd166	f	2026-06-21 18:12:31.229531	2026-06-21 18:12:31.229531	\N	1	\N	\N	\N
0	创建菜单	/api/v1/platform/menu/create	POST	{"name": "测试菜单", "type": 2, "parent_id": 1}	200	{"code": 200, "msg": "创建成功"}	23ms	3	4702eb6a-8692-4f3a-9ee9-3f38a74d9b74	f	2026-06-21 18:12:31.229534	2026-06-21 18:12:31.229534	\N	1	\N	\N	\N
0	更新用户信息	/api/v1/system/user/update/3	PUT	{"name": "普通用户", "status": 0}	200	{"code": 200, "msg": "更新成功"}	18ms	4	a2973ef9-2d8b-4c09-b7e2-488979ba0745	f	2026-06-21 18:12:31.229537	2026-06-21 18:12:31.229538	\N	1	\N	\N	\N
0	创建部门（失败）	/api/v1/system/dept/create	POST	{"name": "测试部门", "parent_id": 1}	400	{"code": 400, "msg": "部门编码已存在"}	8ms	5	ceb8749a-2031-4741-91fc-fced77334134	f	2026-06-21 18:12:31.229541	2026-06-21 18:12:31.229541	\N	1	\N	\N	\N
0	删除角色	/api/v1/system/role/delete	DELETE	{"ids": [5]}	200	{"code": 200, "msg": "删除成功"}	15ms	6	08693d09-d39a-40c4-ab4c-ae64903b1a0d	f	2026-06-21 18:12:31.229544	2026-06-21 18:12:31.229544	\N	1	\N	\N	\N
0	查询菜单列表	/api/v1/platform/menu/list	GET	\N	200	{"code": 200, "data": {"items": [...]}}	35ms	7	a42229e1-7fbd-4586-886b-53d5718dc02f	f	2026-06-21 18:12:31.229547	2026-06-21 18:12:31.229547	\N	3	\N	\N	\N
0	查询字典数据	/api/v1/system/dict/data/list	GET	\N	200	{"code": 200, "data": {"items": [...]}}	22ms	8	e64a26cc-0fb9-45f2-8292-aa3d80510b6b	f	2026-06-21 18:12:31.22955	2026-06-21 18:12:31.22955	\N	3	\N	\N	\N
0	创建工作流	/api/v1/workflow/definition/create	POST	{"name": "审批流程", "code": "approval_v1"}	200	{"code": 200, "msg": "创建成功"}	28ms	9	dc35638d-6dd0-446f-9b29-ded9251a6913	f	2026-06-21 18:12:31.229553	2026-06-21 18:12:31.229553	\N	4	\N	\N	\N
0	创建通知	/api/v1/system/notice/create	POST	{"notice_title": "测试通知", "notice_type": "1"}	200	{"code": 200, "msg": "创建成功"}	11ms	10	cc259886-6df1-41d0-89fe-2cb5fafdecbd	f	2026-06-21 18:12:31.229555	2026-06-21 18:12:31.229556	\N	1	\N	\N	\N
0	导出用户数据	/api/v1/system/user/export	POST	{"status": 0}	200	{"file": "用户列表_20250601.xlsx"}	156ms	11	444d8c52-2abe-431a-8b2c-b7b837516198	f	2026-06-21 18:12:31.229558	2026-06-21 18:12:31.229559	\N	1	\N	\N	\N
0	批量导入用户	/api/v1/system/user/import	POST	"file": "users.xlsx" (multipart/form-data)	200	{"code": 200, "msg": "成功导入 25 条数据"}	320ms	12	1c380b4d-92cf-4d77-9506-8a3e727464b2	f	2026-06-21 18:12:31.229561	2026-06-21 18:12:31.229561	\N	1	\N	\N	\N
0	执行定时任务节点	/api/v1/cronjob/node/execute/1	POST	{"trigger": "now"}	200	{"code": 200, "msg": "调试节点成功"}	1024ms	13	11d96967-dc41-42e1-a894-00be95cf7337	f	2026-06-21 18:12:31.229564	2026-06-21 18:12:31.229564	\N	1	\N	\N	\N
0	执行工作流	/api/v1/workflow/definition/execute	POST	{"workflow_id": 1, "variables": {}}	200	{"code": 200, "data": {"status": "completed"}}	3200ms	14	4ae5c9ae-1467-4e64-a0ec-248e44bc9486	f	2026-06-21 18:12:31.229567	2026-06-21 18:12:31.229567	\N	4	\N	\N	\N
0	批量删除执行日志	/api/v1/cronjob/job/log/delete	DELETE	{"ids": [1, 2, 3]}	200	{"code": 200, "msg": "删除成功"}	19ms	15	5285e6cd-e062-4e54-af86-84e1593c21cf	f	2026-06-21 18:12:31.22957	2026-06-21 18:12:31.22957	\N	1	\N	\N	\N
\.


--
-- Data for Name: sys_param; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_param (config_name, config_key, config_value, config_type, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
演示模式启用	demo_enable	false	t	0	是否启用演示模式	1	6eecabf1-1899-4c3b-9458-1208bded9d19	f	2026-06-21 18:12:31.046616	2026-06-21 18:12:31.046618	\N	1	\N	\N	\N
演示访问IP白名单	ip_white_list	["127.0.0.1", "223.104.209.37"]	t	0	演示模式下允许访问的IP列表	2	2a6d87b5-b02d-4fcd-9c9f-8c4d398d1005	f	2026-06-21 18:12:31.046622	2026-06-21 18:12:31.046623	\N	1	\N	\N	\N
接口白名单	white_api_list_path	["/api/v1/system/auth/login", "/api/v1/system/auth/token/refresh", "/api/v1/system/auth/captcha/get", "/api/v1/system/auth/logout", "/api/v1/system/config/info", "/api/v1/system/user/current/info", "/api/v1/system/notice/available", "/api/v1/system/auth/auto-login/users", "/api/v1/system/auth/auto-login/token", "/api/v1/system/auth/auto-login", "/common/health", "/common/health/ready", "/common/health/live", "/metrics"]	t	0	无需登录即可访问的接口列表	3	228f6c3d-ed8b-40dc-ab78-6463e13864e1	f	2026-06-21 18:12:31.046625	2026-06-21 18:12:31.046626	\N	1	\N	\N	\N
访问IP黑名单	ip_black_list	[]	t	0	禁止访问的IP列表	4	46097a45-32e3-4f4c-911c-ded233a8aae7	f	2026-06-21 18:12:31.046628	2026-06-21 18:12:31.046629	\N	1	\N	\N	\N
登录失败次数限制	login_failed_limit	5	t	0	登录失败最大次数	5	2313d88c-4dea-4381-9d80-ecbfe79b84b5	f	2026-06-21 18:12:31.046632	2026-06-21 18:12:31.046632	\N	1	\N	\N	\N
登录锁定时间(分钟)	login_lock_time	15	t	0	登录失败后锁定时间	6	22fb9ba0-94d9-46f1-bf45-1355e22f9e69	f	2026-06-21 18:12:31.046635	2026-06-21 18:12:31.046635	\N	1	\N	\N	\N
Token过期时间(分钟)	token_expire_minutes	120	t	0	Access Token过期时间	7	462dc745-0d3c-47d5-bd3d-fc712b42f369	f	2026-06-21 18:12:31.046638	2026-06-21 18:12:31.046638	\N	1	\N	\N	\N
Refresh Token过期时间(天)	refresh_token_expire_days	7	t	0	Refresh Token过期时间	8	94986d26-7cfd-44e2-8e82-45cd6c0fa8d0	f	2026-06-21 18:12:31.04664	2026-06-21 18:12:31.046641	\N	1	\N	\N	\N
密码有效期(天)	password_expire_days	90	t	0	密码有效期	9	100d4e26-a7f1-4c1c-8efb-c206fae998db	f	2026-06-21 18:12:31.046643	2026-06-21 18:12:31.046644	\N	1	\N	\N	\N
密码最小长度	password_min_length	6	t	0	密码最小长度	10	b1361dc1-81f9-4c4d-8e59-e91ab8cf8f30	f	2026-06-21 18:12:31.046646	2026-06-21 18:12:31.046647	\N	1	\N	\N	\N
是否启用验证码	captcha_enable	true	t	0	登录时是否启用验证码	11	cee9f10f-8bb5-4ebf-8090-afcd30858c32	f	2026-06-21 18:12:31.046649	2026-06-21 18:12:31.04665	\N	1	\N	\N	\N
是否记录操作日志	operation_log_enable	true	t	0	是否记录用户操作日志	12	615604ac-b4c0-49b5-8174-0b881b23cc29	f	2026-06-21 18:12:31.046652	2026-06-21 18:12:31.046653	\N	1	\N	\N	\N
操作日志保留天数	operation_log_retention_days	90	t	0	操作日志保留天数	13	ce602d51-adc9-4d72-82a3-06bc74812168	f	2026-06-21 18:12:31.046655	2026-06-21 18:12:31.046656	\N	1	\N	\N	\N
登录日志保留天数	login_log_retention_days	30	t	0	登录日志保留天数	14	f12747fb-406e-4aad-84fd-f0ba18d2cb26	f	2026-06-21 18:12:31.046658	2026-06-21 18:12:31.046659	\N	1	\N	\N	\N
文件上传大小限制(MB)	file_upload_max_size	50	t	0	单个文件上传最大大小	15	2da642a3-813e-42af-bbcc-6b88926fa536	f	2026-06-21 18:12:31.046661	2026-06-21 18:12:31.046662	\N	1	\N	\N	\N
是否启用IP归属地查询	ip_location_enable	false	t	0	登录时是否查询IP归属地	16	0f621411-0a91-4b73-a450-990c922286c1	f	2026-06-21 18:12:31.046665	2026-06-21 18:12:31.046665	\N	1	\N	\N	\N
调度器状态	scheduler_status	stopped	t	0	\N	17	db58af45-013a-4b0b-b765-4c7aff949a73	f	2026-06-21 18:12:34.011911	2026-06-21 18:12:34.011914	\N	1	\N	\N	\N
\.


--
-- Data for Name: sys_position; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_position (name, code, "order", status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
技术总监	TECH_DIRECTOR	1	0	技术部门负责人	1	a9f4660b-3f38-4a1c-9d8e-f9dd2624b826	f	2026-06-21 18:12:31.100645	2026-06-21 18:12:31.100649	\N	1	\N	\N	\N
高级工程师	SR_ENGINEER	2	0	高级技术岗位	2	a3b75476-0b00-489c-9028-f9a690fe4209	f	2026-06-21 18:12:31.100653	2026-06-21 18:12:31.100654	\N	1	\N	\N	\N
工程师	ENGINEER	3	0	技术岗位	3	bcabe625-015c-4851-9438-86c3b1c2cf36	f	2026-06-21 18:12:31.100657	2026-06-21 18:12:31.100657	\N	1	\N	\N	\N
产品经理	PRODUCT_MANAGER	4	0	产品管理岗位	4	c34c3ea4-7d76-4ab0-9620-934f4aa22067	f	2026-06-21 18:12:31.10066	2026-06-21 18:12:31.10066	\N	1	\N	\N	\N
运营专员	OPERATOR	5	0	运营岗位	5	97645a0a-7cde-45b1-8be7-932367ceafb3	f	2026-06-21 18:12:31.100663	2026-06-21 18:12:31.100663	\N	1	\N	\N	\N
HR专员	HR_STAFF	6	0	人事专员	6	5ba9b102-0031-4554-b5fc-708dbe060e06	f	2026-06-21 18:12:31.100666	2026-06-21 18:12:31.100666	\N	1	\N	\N	\N
\.


--
-- Data for Name: sys_role; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_role (name, code, "order", status, description, data_scope, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
超级管理员	SUPER_ADMIN	1	0	拥有系统最高权限	4	1	7843a175-2712-44a5-9599-d8819c381f58	f	2026-06-21 18:12:31.072906	2026-06-21 18:12:31.07291	\N	1	\N	\N	\N
管理员	ADMIN	2	0	管理租户内所有资源	3	2	303d84bd-59dc-4972-b431-e450596c75eb	f	2026-06-21 18:12:31.072914	2026-06-21 18:12:31.072914	\N	1	\N	\N	\N
普通用户	USER	3	0	仅能查看和操作自己的数据	1	3	dd390f90-00ce-4c12-8b3d-3d400bdabf17	f	2026-06-21 18:12:31.072917	2026-06-21 18:12:31.072918	\N	1	\N	\N	\N
星辰管理员	STAR_ADMIN	1	0	星辰科技有限公司管理员	4	4	4e97ab33-aef3-416a-a886-99458aea5a37	f	2026-06-21 18:12:31.072921	2026-06-21 18:12:31.072921	\N	3	\N	\N	\N
星辰员工	STAR_STAFF	2	0	星辰科技有限公司普通员工	2	5	31e6f4c2-5ff8-4161-bf84-de3ba68dce87	f	2026-06-21 18:12:31.072924	2026-06-21 18:12:31.072924	\N	3	\N	\N	\N
创新管理员	INNO_ADMIN	1	0	创新工坊管理员	4	6	cf7c56a8-2476-48af-9353-f1419d291005	f	2026-06-21 18:12:31.072927	2026-06-21 18:12:31.072927	\N	4	\N	\N	\N
创新员工	INNO_STAFF	2	0	创新工坊普通员工	2	7	e967ee5f-3058-4a1e-b5e1-70640eb837d8	f	2026-06-21 18:12:31.07293	2026-06-21 18:12:31.07293	\N	4	\N	\N	\N
\.


--
-- Data for Name: sys_role_depts; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_role_depts (role_id, dept_id) FROM stdin;
\.


--
-- Data for Name: sys_role_menus; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_role_menus (role_id, menu_id) FROM stdin;
\.


--
-- Data for Name: sys_ticket; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_ticket (title, status, description, ticket_content, summary, ticket_type, images, reply, assigned_id, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
系统登录页面优化建议	2	用户体验优化	<p>建议在登录页面增加记住密码功能和第三方登录入口，提升用户体验。</p>	建议在登录页面增加记住密码功能和第三方登录入口	suggestion	\N	感谢您的建议，我们将在下个版本中加入记住密码功能。	2	1	297964e4-81cb-4fae-bed8-64aff490503d	f	2026-06-21 18:12:31.209627	2026-06-21 18:12:31.209629	\N	1	\N	\N	\N
表格导出功能异常	1	导出功能问题	<p>当数据量超过1000条时，导出Excel功能会超时失败。</p>	数据量超过1000条导出Excel超时	bug	\N	\N	3	2	8f3ce999-72ba-4621-b594-bf3fc19e6200	f	2026-06-21 18:12:31.209632	2026-06-21 18:12:31.209633	\N	1	\N	\N	\N
希望增加批量删除功能	0	功能优化建议	<p>用户管理页面希望支持批量选择删除，提高管理效率。</p>	用户管理页面希望支持批量选择删除	optimize	\N	\N	\N	3	3e83b81f-f30f-4475-9857-39e390748e79	f	2026-06-21 18:12:31.209636	2026-06-21 18:12:31.209636	\N	1	\N	\N	\N
手机端适配问题反馈	1	移动端兼容性问题	<p>在iPhone Safari浏览器上，菜单栏折叠后无法展开，需要刷新页面才能恢复。</p>	iPhone Safari菜单折叠后无法展开	bug	["https://example.com/screenshot1.png"]	\N	4	4	1fba9443-0897-40c7-938e-f3b4daec930c	f	2026-06-21 18:12:31.209639	2026-06-21 18:12:31.209639	\N	1	\N	\N	\N
增加数据权限粒度	2	数据权限增强	<p>当前数据权限只能控制到部门级别，希望能支持自定义数据范围，如只查看本人创建的数据、指定项目范围等。</p>	数据权限需要支持自定义范围	optimize	\N	已纳入Q3规划，感谢反馈。	2	5	92b09ed2-9747-4ea7-aa53-6603b7a6ee05	f	2026-06-21 18:12:31.209642	2026-06-21 18:12:31.209642	\N	1	\N	\N	\N
工作流审批节点无法修改	0	星辰科技反馈工作流问题	<p>已发布的工作流无法修改审批节点配置，需要先取消发布才能修改，操作繁琐。</p>	已发布工作流无法直接修改节点	bug	\N	\N	\N	6	98ab6624-2736-4089-ae88-e190a999bf00	f	2026-06-21 18:12:31.209645	2026-06-21 18:12:31.209645	\N	3	\N	\N	\N
希望增加钉钉集成	3	创新工坊第三方集成需求	<p>团队使用钉钉进行日常协作，希望能将通知和待办事项同步到钉钉工作台。</p>	希望支持钉钉消息集成	suggestion	\N	我们会评估第三方集成的优先级。	\N	7	27e3e16b-236f-47a8-b4b3-7a12f0cf992e	f	2026-06-21 18:12:31.209648	2026-06-21 18:12:31.209648	\N	4	\N	\N	\N
其他-文档链接失效	0	文档链接问题	<p>帮助文档中的API接口说明链接跳转404，影响开发对接。</p>	帮助文档API链接404	other	\N	\N	3	8	3a0cebba-e55f-464e-b694-7cc5ee802137	f	2026-06-21 18:12:31.20965	2026-06-21 18:12:31.209651	\N	1	\N	\N	\N
\.


--
-- Data for Name: sys_user; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_user (username, password, name, mobile, email, gender, avatar, is_superuser, last_login, gitee_login, github_login, wx_login, qq_login, status, description, dept_id, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
super	$pbkdf2-sha256$600000$XX20aO1v73xS0JnoewXNtw==$PEaVHV1N5L7PfYQw2lCAQOc4hAEyCiwsGR48/jgVBjU=	超级管理员	13800138000	super@example.com	0	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	t	\N	\N	\N	\N	\N	0	系统超级管理员	1	1	dea2a3ed-3d26-479f-a162-68ff50303bd2	f	2026-06-21 18:12:31.108032	2026-06-21 18:12:31.108035	\N	1	\N	\N	\N
admin	$pbkdf2-sha256$600000$XX20aO1v73xS0JnoewXNtw==$PEaVHV1N5L7PfYQw2lCAQOc4hAEyCiwsGR48/jgVBjU=	管理员	13800138001	admin@example.com	0	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	t	\N	\N	\N	\N	\N	0	技术部门管理员	2	2	fec08ea4-4acd-487a-a27e-015540f57c26	f	2026-06-21 18:12:31.108039	2026-06-21 18:12:31.108039	\N	1	1	\N	\N
user	$pbkdf2-sha256$600000$XX20aO1v73xS0JnoewXNtw==$PEaVHV1N5L7PfYQw2lCAQOc4hAEyCiwsGR48/jgVBjU=	普通用户	13800138002	user@example.com	0	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	f	\N	\N	\N	\N	\N	0	后端开发工程师	3	3	357600ed-3fbc-461e-a61f-b3ebbee8cdf6	f	2026-06-21 18:12:31.108042	2026-06-21 18:12:31.108043	\N	1	1	\N	\N
product	$pbkdf2-sha256$600000$XX20aO1v73xS0JnoewXNtw==$PEaVHV1N5L7PfYQw2lCAQOc4hAEyCiwsGR48/jgVBjU=	产品经理	13800138003	product@example.com	1	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	f	\N	\N	\N	\N	\N	0	产品经理	5	4	8e496c4a-125b-4653-9e73-7d660804200b	f	2026-06-21 18:12:31.108046	2026-06-21 18:12:31.108046	\N	1	1	\N	\N
hr	$pbkdf2-sha256$600000$XX20aO1v73xS0JnoewXNtw==$PEaVHV1N5L7PfYQw2lCAQOc4hAEyCiwsGR48/jgVBjU=	HR专员	13800138004	hr@example.com	1	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	f	\N	\N	\N	\N	\N	0	人力资源专员	6	5	f9f472e6-c7bc-403c-a1fd-16a38116db91	f	2026-06-21 18:12:31.108049	2026-06-21 18:12:31.108049	\N	1	1	\N	\N
zhang_admin	$pbkdf2-sha256$600000$E8jfd18sWu7N9DWsx/nYKg==$9DNKCv+dm1QDvYXwpQlZH6e7trYp1WCPdsvSyzXwuo0=	张明	13800001001	zhang@star-tech.dev	2	\N	f	\N	\N	\N	\N	\N	0	星辰科技管理员	\N	6	06a1dfea-2824-48f6-a71a-69e3ed17a61e	f	2026-06-21 18:12:31.11198	2026-06-21 18:12:31.111982	\N	3	\N	\N	\N
wang_dev	$pbkdf2-sha256$600000$E8jfd18sWu7N9DWsx/nYKg==$9DNKCv+dm1QDvYXwpQlZH6e7trYp1WCPdsvSyzXwuo0=	王华	13800001002	wang@star-tech.dev	2	\N	f	\N	\N	\N	\N	\N	0	星辰科技研发工程师	\N	7	c515992e-986a-4101-b448-5dd520069718	f	2026-06-21 18:12:31.111986	2026-06-21 18:12:31.111987	\N	3	\N	\N	\N
li_admin	$pbkdf2-sha256$600000$E8jfd18sWu7N9DWsx/nYKg==$9DNKCv+dm1QDvYXwpQlZH6e7trYp1WCPdsvSyzXwuo0=	李芳	13800002001	li@inno.work	2	\N	f	\N	\N	\N	\N	\N	0	创新工坊创始人	\N	8	a15f44e0-899f-475d-ba1d-ce62a3a26cbd	f	2026-06-21 18:12:31.11199	2026-06-21 18:12:31.11199	\N	4	\N	\N	\N
zhao_eng	$pbkdf2-sha256$600000$E8jfd18sWu7N9DWsx/nYKg==$9DNKCv+dm1QDvYXwpQlZH6e7trYp1WCPdsvSyzXwuo0=	赵强	13800002002	zhao@inno.work	2	\N	f	\N	\N	\N	\N	\N	0	创新工坊技术合伙人	\N	9	03ef8fb6-d675-4270-b34f-63b53489c517	f	2026-06-21 18:12:31.111993	2026-06-21 18:12:31.111993	\N	4	\N	\N	\N
\.


--
-- Data for Name: sys_user_positions; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_user_positions (user_id, position_id) FROM stdin;
\.


--
-- Data for Name: sys_user_roles; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_user_roles (user_id, role_id) FROM stdin;
1	1
2	2
3	3
4	3
5	3
6	4
7	5
8	6
9	7
\.


--
-- Data for Name: task_job; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.task_job (job_id, job_name, trigger_type, next_run_time, job_state, result, error, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id) FROM stdin;
system_tenant_expiry_check	租户到期检查	interval	2026-06-21 19:12:31.401289+08:00	{\n  "version": 1,\n  "id": "system_tenant_expiry_check",\n  "func": "app.api.v1.module_platform.tenant.service:TenantService.check_tenant_expiry",\n  "trigger": "interval[1:00:00]",\n  "executor": "default",\n  "args": [],\n  "kwargs": {},\n  "name": "租户到期检查",\n  "misfire_grace_time": 1,\n  "coalesce": true,\n  "max_instances": 5,\n  "next_run_time": "2026-06-21 19:12:31.401289+08:00"\n}	\N	\N	0	\N	1	838d8e40-7fc8-4cfc-a8da-cdfe83c55aa7	f	2026-06-21 18:12:31.406262	2026-06-21 18:12:31.406265	\N	1
system_grace_reminder	宽限期续费提醒	cron	2026-06-22 09:00:00+08:00	{\n  "version": 1,\n  "id": "system_grace_reminder",\n  "func": "app.api.v1.module_platform.tenant.service:TenantService.send_grace_reminders",\n  "trigger": "cron[hour='9', minute='0']",\n  "executor": "default",\n  "args": [],\n  "kwargs": {},\n  "name": "宽限期续费提醒",\n  "misfire_grace_time": 1,\n  "coalesce": true,\n  "max_instances": 5,\n  "next_run_time": "2026-06-22 09:00:00+08:00"\n}	\N	\N	0	\N	2	888cc4e0-6a9b-4fd1-8a9e-55e92bbaa840	f	2026-06-21 18:12:31.422446	2026-06-21 18:12:31.42245	\N	1
system_clean_expired	过期租户归档清理	cron	2026-07-01 02:00:00+08:00	{\n  "version": 1,\n  "id": "system_clean_expired",\n  "func": "app.api.v1.module_platform.tenant.service:TenantService.clean_expired_tenants",\n  "trigger": "cron[day='1', hour='2', minute='0']",\n  "executor": "default",\n  "args": [],\n  "kwargs": {},\n  "name": "过期租户归档清理",\n  "misfire_grace_time": 1,\n  "coalesce": true,\n  "max_instances": 5,\n  "next_run_time": "2026-07-01 02:00:00+08:00"\n}	\N	\N	0	\N	3	e1dace15-030e-4a37-8c05-69db251194a0	f	2026-06-21 18:12:31.428059	2026-06-21 18:12:31.42806	\N	1
system_cancel_expired_orders	超时订单取消	interval	2026-06-21 18:17:31.432632+08:00	{\n  "version": 1,\n  "id": "system_cancel_expired_orders",\n  "func": "app.api.v1.module_platform.order.service:OrderService.cancel_expired_orders",\n  "trigger": "interval[0:05:00]",\n  "executor": "default",\n  "args": [],\n  "kwargs": {},\n  "name": "超时订单取消",\n  "misfire_grace_time": 1,\n  "coalesce": true,\n  "max_instances": 5,\n  "next_run_time": "2026-06-21 18:17:31.432632+08:00"\n}	\N	\N	0	\N	4	3de25fe8-92ef-429f-9bab-f868173f4cb2	f	2026-06-21 18:12:31.434109	2026-06-21 18:12:31.43411	\N	1
system_cleanup_operation_log	操作日志清理	cron	2026-06-28 03:00:00+08:00	{\n  "version": 1,\n  "id": "system_cleanup_operation_log",\n  "func": "app.api.v1.module_system.log.service:OperationLogService.cleanup_operation_log",\n  "trigger": "cron[day_of_week='sun', hour='3', minute='0']",\n  "executor": "default",\n  "args": [],\n  "kwargs": {},\n  "name": "操作日志清理",\n  "misfire_grace_time": 1,\n  "coalesce": true,\n  "max_instances": 5,\n  "next_run_time": "2026-06-28 03:00:00+08:00"\n}	\N	\N	0	\N	5	b1060d82-e5b8-40e0-b32c-2152b9831fd7	f	2026-06-21 18:12:31.437878	2026-06-21 18:12:31.437879	\N	1
\.


--
-- Data for Name: task_node; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.task_node (name, code, jobstore, executor, trigger, trigger_args, func, args, kwargs, "coalesce", max_instances, start_date, end_date, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
演示任务	demo_job	default	default	\N	\N	import logging\n\ndef handler(*args, **kwargs):\n    """演示任务：打印参数并返回执行摘要"""\n    logger = logging.getLogger(__name__)\n    logger.info(f"演示任务执行中，参数: args={args}, kwargs={kwargs}")\n    return {\n        "status": "success",\n        "message": "演示任务执行成功",\n        "args_received": len(args),\n        "kwargs_keys": list(kwargs.keys())\n    }\n	\N	\N	f	1	\N	\N	0	最简演示任务，用于验证调度器基本功能	1	ef150683-e66e-4ad5-b6e6-2d6207345a6c	f	2026-06-21 18:12:31.239151	2026-06-21 18:12:31.239155	\N	1	\N	\N	\N
数据库清理任务	db_cleanup	sqlalchemy	default	\N	\N	import logging\nfrom datetime import datetime, timedelta\n\ndef handler(*args, **kwargs):\n    """清理过期数据：删除N天前的日志和临时数据"""\n    logger = logging.getLogger(__name__)\n    days = kwargs.get("days", 90)\n    cutoff = datetime.now() - timedelta(days=days)\n    logger.info(f"清理 {cutoff.strftime('%Y-%m-%d')} 之前的过期数据...")\n    return {\n        "status": "success",\n        "cutoff_date": cutoff.strftime("%Y-%m-%d %H:%M:%S"),\n        "deleted_count": 0\n    }\n	\N	{"days": 30}	t	1	\N	\N	0	清理过期操作日志和临时数据，建议每天凌晨3点执行	2	f1645b41-a100-40ae-a9a4-e70ea82bb4b9	f	2026-06-21 18:12:31.239159	2026-06-21 18:12:31.23916	\N	1	\N	\N	\N
健康检查任务	health_check	default	default	\N	\N	import logging\nimport psutil\n\ndef handler(*args, **kwargs):\n    """系统健康检查：采集 CPU、内存、磁盘使用率"""\n    logger = logging.getLogger(__name__)\n    cpu = psutil.cpu_percent(interval=1)\n    mem = psutil.virtual_memory()\n    disk = psutil.disk_usage("/")\n    status = "healthy" if cpu < 80 and mem.percent < 90 and disk.percent < 90 else "warning"\n    logger.info(f"健康检查: CPU={cpu}% MEM={mem.percent}% DISK={disk.percent}%")\n    return {\n        "status": status,\n        "cpu_percent": cpu,\n        "memory_percent": mem.percent,\n        "disk_percent": disk.percent,\n        "memory_total_gb": round(mem.total / (1024**3), 1),\n        "disk_total_gb": round(disk.total / (1024**3), 1)\n    }\n	\N	\N	t	1	\N	\N	0	系统资源健康检查，建议每5分钟执行一次	3	018980c1-4365-461d-9710-846dee15ca62	f	2026-06-21 18:12:31.239163	2026-06-21 18:12:31.239164	\N	1	\N	\N	\N
邮件批量发送	email_batch	sqlalchemy	default	\N	\N	import logging\n\ndef handler(*args, **kwargs):\n    """批量发送待发送邮件"""\n    logger = logging.getLogger(__name__)\n    batch_size = kwargs.get("batch_size", 50)\n    logger.info(f"开始批量发送邮件，每批 {batch_size} 封...")\n    return {\n        "status": "success",\n        "sent_count": 0,\n        "failed_count": 0,\n        "batch_size": batch_size\n    }\n	\N	{"batch_size": 50}	f	2	\N	\N	0	批量发送待发送邮件，建议每分钟执行一次	4	ac14c414-4b8a-4147-a9a6-6eedd54db09e	f	2026-06-21 18:12:31.239166	2026-06-21 18:12:31.239167	\N	1	\N	\N	\N
\.


--
-- Data for Name: task_workflow; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.task_workflow (name, code, nodes, edges, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
\.


--
-- Data for Name: task_workflow_node_type; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.task_workflow_node_type (name, code, category, func, args, kwargs, sort_order, is_active, status, description, id, uuid, is_deleted, created_time, updated_time, deleted_time, tenant_id, created_id, updated_id, deleted_id) FROM stdin;
HTTP请求	http_request	action	import json\nimport urllib.request\n\ndef handler(*args, **kwargs):\n    """发送 HTTP 请求并返回响应"""\n    url = kwargs.get("url", "")\n    method = kwargs.get("method", "GET")\n    headers = kwargs.get("headers", {})\n    body = kwargs.get("body")\n    if not url:\n        raise ValueError("缺少 url 参数")\n    req = urllib.request.Request(url, method=method, headers=headers)\n    if body and isinstance(body, dict):\n        req.data = json.dumps(body).encode()\n    with urllib.request.urlopen(req) as resp:\n        return {"status_code": resp.status, "body": resp.read().decode()}\n	\N	{"url": "", "method": "GET"}	1	t	0	发送 HTTP 请求，支持 GET/POST 等方法	1	2fd5124d-fd0f-43fb-83d6-baea01f44fba	f	2026-06-21 18:12:31.246264	2026-06-21 18:12:31.246266	\N	1	\N	\N	\N
发送通知	send_notification	action	import logging\n\ndef handler(*args, **kwargs):\n    """发送通知消息"""\n    logger = logging.getLogger(__name__)\n    channel = kwargs.get("channel", "system")\n    title = kwargs.get("title", "工作流通知")\n    content = kwargs.get("content", "")\n    recipients = kwargs.get("recipients", [])\n    logger.info(f"[{channel}] 发送通知: {title} -> {len(recipients)}人")\n    return {\n        "channel": channel,\n        "title": title,\n        "recipient_count": len(recipients),\n        "status": "sent"\n    }\n	\N	{"channel": "system", "title": "工作流通知", "recipients": []}	2	t	0	发送系统通知、邮件或短信	2	2c7baf02-b855-443b-9529-5a6ef9790059	f	2026-06-21 18:12:31.24627	2026-06-21 18:12:31.24627	\N	1	\N	\N	\N
条件判断	condition	condition	import json\n\ndef handler(*args, **kwargs):\n    """条件分支：根据 upstream 结果决定走向"""\n    upstream = kwargs.get("upstream", {})\n    variables = kwargs.get("variables", {})\n    field = kwargs.get("field", "status")\n    expected = kwargs.get("expected", "success")\n    operator = kwargs.get("operator", "eq")\n    last = list(upstream.values())[-1] if upstream else {}\n    actual = last.get(field) if isinstance(last, dict) else last\n    operations = {\n        "eq": lambda a, e: a == e,\n        "ne": lambda a, e: a != e,\n        "gt": lambda a, e: a > e,\n        "lt": lambda a, e: a < e,\n        "contains": lambda a, e: str(e) in str(a)\n    }\n    op = operations.get(operator, operations["eq"])\n    result = op(actual, expected)\n    return {"passed": result, "actual": actual, "expected": expected}\n	\N	{"field": "status", "expected": "success", "operator": "eq"}	3	t	0	根据上游节点输出判断分支走向	3	e6d33519-9e26-47d5-b17b-01924fd80c54	f	2026-06-21 18:12:31.246273	2026-06-21 18:12:31.246274	\N	1	\N	\N	\N
数据转换	data_transform	action	import json\nfrom datetime import datetime\n\ndef handler(*args, **kwargs):\n    """转换上游数据格式"""\n    upstream = kwargs.get("upstream", {})\n    mapping = kwargs.get("mapping", {})\n    result = {}\n    for upstream_key, target_key in mapping.items():\n        for source, value in upstream.items():\n            if isinstance(value, dict) and upstream_key in value:\n                result[target_key] = value[upstream_key]\n    result["transformed_at"] = datetime.now().isoformat()\n    return result\n	\N	{"mapping": {}}	4	t	0	转换上游节点的数据格式	4	ed9dd777-59ec-4b40-911a-3cc84bdefe56	f	2026-06-21 18:12:31.246276	2026-06-21 18:12:31.246277	\N	1	\N	\N	\N
聚合汇总	aggregate	action	import json\n\ndef handler(*args, **kwargs):\n    """聚合上游多个节点的输出"""\n    upstream = kwargs.get("upstream", {})\n    variables = kwargs.get("variables", {})\n    results = {\n        "node_count": len(upstream),\n        "nodes": list(upstream.keys()),\n        "values": list(upstream.values()),\n        "variables": variables\n    }\n    return results\n	\N	\N	5	t	0	将多个上游节点的输出聚合到一个结果中	5	9edb01bf-27c7-4339-af25-085d5d1592f3	f	2026-06-21 18:12:31.246279	2026-06-21 18:12:31.24628	\N	1	\N	\N	\N
\.


--
-- Name: example_demo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.example_demo_id_seq', 6, true);


--
-- Name: gen_table_column_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.gen_table_column_id_seq', 1, false);


--
-- Name: gen_table_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.gen_table_id_seq', 1, false);


--
-- Name: platform_email_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_email_config_id_seq', 1, true);


--
-- Name: platform_email_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_email_log_id_seq', 1, false);


--
-- Name: platform_email_template_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_email_template_id_seq', 12, true);


--
-- Name: platform_invoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_invoice_id_seq', 4, true);


--
-- Name: platform_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_menu_id_seq', 220, true);


--
-- Name: platform_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_order_id_seq', 9, true);


--
-- Name: platform_package_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_package_id_seq', 4, true);


--
-- Name: platform_package_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_package_menu_id_seq', 30, true);


--
-- Name: platform_package_plugin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_package_plugin_id_seq', 1, false);


--
-- Name: platform_payment_record_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_payment_record_id_seq', 7, true);


--
-- Name: platform_plugin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_plugin_id_seq', 5, true);


--
-- Name: platform_refund_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_refund_id_seq', 1, true);


--
-- Name: platform_tenant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_tenant_id_seq', 4, true);


--
-- Name: platform_tenant_plugin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_tenant_plugin_id_seq', 8, true);


--
-- Name: platform_user_tenant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.platform_user_tenant_id_seq', 10, true);


--
-- Name: sys_dept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_dept_id_seq', 13, true);


--
-- Name: sys_dict_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_dict_data_id_seq', 34, true);


--
-- Name: sys_dict_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_dict_type_id_seq', 10, true);


--
-- Name: sys_login_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_login_log_id_seq', 12, true);


--
-- Name: sys_notice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_notice_id_seq', 6, true);


--
-- Name: sys_operation_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_operation_log_id_seq', 15, true);


--
-- Name: sys_param_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_param_id_seq', 17, true);


--
-- Name: sys_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_position_id_seq', 6, true);


--
-- Name: sys_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_role_id_seq', 7, true);


--
-- Name: sys_ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_ticket_id_seq', 8, true);


--
-- Name: sys_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_user_id_seq', 9, true);


--
-- Name: task_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.task_job_id_seq', 5, true);


--
-- Name: task_node_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.task_node_id_seq', 4, true);


--
-- Name: task_workflow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.task_workflow_id_seq', 1, false);


--
-- Name: task_workflow_node_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.task_workflow_node_type_id_seq', 5, true);


--
-- Name: apscheduler_jobs apscheduler_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.apscheduler_jobs
    ADD CONSTRAINT apscheduler_jobs_pkey PRIMARY KEY (id);


--
-- Name: example_demo example_demo_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.example_demo
    ADD CONSTRAINT example_demo_pkey PRIMARY KEY (id);


--
-- Name: gen_table_column gen_table_column_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_pkey PRIMARY KEY (id);


--
-- Name: gen_table gen_table_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_pkey PRIMARY KEY (id);


--
-- Name: platform_email_config platform_email_config_name_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_config
    ADD CONSTRAINT platform_email_config_name_key UNIQUE (name);


--
-- Name: platform_email_config platform_email_config_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_config
    ADD CONSTRAINT platform_email_config_pkey PRIMARY KEY (id);


--
-- Name: platform_email_log platform_email_log_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_log
    ADD CONSTRAINT platform_email_log_pkey PRIMARY KEY (id);


--
-- Name: platform_email_template platform_email_template_name_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_template
    ADD CONSTRAINT platform_email_template_name_key UNIQUE (name);


--
-- Name: platform_email_template platform_email_template_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_template
    ADD CONSTRAINT platform_email_template_pkey PRIMARY KEY (id);


--
-- Name: platform_email_template platform_email_template_template_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_template
    ADD CONSTRAINT platform_email_template_template_code_key UNIQUE (template_code);


--
-- Name: platform_invoice platform_invoice_invoice_no_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_invoice
    ADD CONSTRAINT platform_invoice_invoice_no_key UNIQUE (invoice_no);


--
-- Name: platform_invoice platform_invoice_order_id_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_invoice
    ADD CONSTRAINT platform_invoice_order_id_key UNIQUE (order_id);


--
-- Name: platform_invoice platform_invoice_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_invoice
    ADD CONSTRAINT platform_invoice_pkey PRIMARY KEY (id);


--
-- Name: platform_menu platform_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_menu
    ADD CONSTRAINT platform_menu_pkey PRIMARY KEY (id);


--
-- Name: platform_order platform_order_order_no_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_order
    ADD CONSTRAINT platform_order_order_no_key UNIQUE (order_no);


--
-- Name: platform_order platform_order_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_order
    ADD CONSTRAINT platform_order_pkey PRIMARY KEY (id);


--
-- Name: platform_package platform_package_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package
    ADD CONSTRAINT platform_package_code_key UNIQUE (code);


--
-- Name: platform_package_menu platform_package_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package_menu
    ADD CONSTRAINT platform_package_menu_pkey PRIMARY KEY (id);


--
-- Name: platform_package platform_package_name_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package
    ADD CONSTRAINT platform_package_name_key UNIQUE (name);


--
-- Name: platform_package platform_package_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package
    ADD CONSTRAINT platform_package_pkey PRIMARY KEY (id);


--
-- Name: platform_package_plugin platform_package_plugin_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package_plugin
    ADD CONSTRAINT platform_package_plugin_pkey PRIMARY KEY (id);


--
-- Name: platform_payment_record platform_payment_record_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_payment_record
    ADD CONSTRAINT platform_payment_record_pkey PRIMARY KEY (id);


--
-- Name: platform_payment_record platform_payment_record_transaction_id_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_payment_record
    ADD CONSTRAINT platform_payment_record_transaction_id_key UNIQUE (transaction_id);


--
-- Name: platform_plugin platform_plugin_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_plugin
    ADD CONSTRAINT platform_plugin_code_key UNIQUE (code);


--
-- Name: platform_plugin platform_plugin_name_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_plugin
    ADD CONSTRAINT platform_plugin_name_key UNIQUE (name);


--
-- Name: platform_plugin platform_plugin_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_plugin
    ADD CONSTRAINT platform_plugin_pkey PRIMARY KEY (id);


--
-- Name: platform_refund platform_refund_order_id_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_refund
    ADD CONSTRAINT platform_refund_order_id_key UNIQUE (order_id);


--
-- Name: platform_refund platform_refund_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_refund
    ADD CONSTRAINT platform_refund_pkey PRIMARY KEY (id);


--
-- Name: platform_refund platform_refund_refund_no_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_refund
    ADD CONSTRAINT platform_refund_refund_no_key UNIQUE (refund_no);


--
-- Name: platform_tenant platform_tenant_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_tenant
    ADD CONSTRAINT platform_tenant_code_key UNIQUE (code);


--
-- Name: platform_tenant platform_tenant_name_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_tenant
    ADD CONSTRAINT platform_tenant_name_key UNIQUE (name);


--
-- Name: platform_tenant platform_tenant_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_tenant
    ADD CONSTRAINT platform_tenant_pkey PRIMARY KEY (id);


--
-- Name: platform_tenant_plugin platform_tenant_plugin_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_tenant_plugin
    ADD CONSTRAINT platform_tenant_plugin_pkey PRIMARY KEY (id);


--
-- Name: platform_user_tenant platform_user_tenant_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_user_tenant
    ADD CONSTRAINT platform_user_tenant_pkey PRIMARY KEY (id);


--
-- Name: sys_dept sys_dept_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_pkey PRIMARY KEY (id);


--
-- Name: sys_dept sys_dept_tenant_id_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_tenant_id_code_key UNIQUE (tenant_id, code);


--
-- Name: sys_dict_data sys_dict_data_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_pkey PRIMARY KEY (id);


--
-- Name: sys_dict_type sys_dict_type_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_type
    ADD CONSTRAINT sys_dict_type_pkey PRIMARY KEY (id);


--
-- Name: sys_dict_type sys_dict_type_tenant_id_dict_type_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_type
    ADD CONSTRAINT sys_dict_type_tenant_id_dict_type_key UNIQUE (tenant_id, dict_type);


--
-- Name: sys_login_log sys_login_log_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_login_log
    ADD CONSTRAINT sys_login_log_pkey PRIMARY KEY (id);


--
-- Name: sys_notice sys_notice_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_pkey PRIMARY KEY (id);


--
-- Name: sys_operation_log sys_operation_log_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_operation_log
    ADD CONSTRAINT sys_operation_log_pkey PRIMARY KEY (id);


--
-- Name: sys_param sys_param_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_param
    ADD CONSTRAINT sys_param_pkey PRIMARY KEY (id);


--
-- Name: sys_position sys_position_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_pkey PRIMARY KEY (id);


--
-- Name: sys_role_depts sys_role_depts_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role_depts
    ADD CONSTRAINT sys_role_depts_pkey PRIMARY KEY (role_id, dept_id);


--
-- Name: sys_role_menus sys_role_menus_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role_menus
    ADD CONSTRAINT sys_role_menus_pkey PRIMARY KEY (role_id, menu_id);


--
-- Name: sys_role sys_role_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role
    ADD CONSTRAINT sys_role_pkey PRIMARY KEY (id);


--
-- Name: sys_role sys_role_tenant_id_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role
    ADD CONSTRAINT sys_role_tenant_id_code_key UNIQUE (tenant_id, code);


--
-- Name: sys_ticket sys_ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_ticket
    ADD CONSTRAINT sys_ticket_pkey PRIMARY KEY (id);


--
-- Name: sys_user sys_user_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_pkey PRIMARY KEY (id);


--
-- Name: sys_user_positions sys_user_positions_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user_positions
    ADD CONSTRAINT sys_user_positions_pkey PRIMARY KEY (user_id, position_id);


--
-- Name: sys_user_roles sys_user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user_roles
    ADD CONSTRAINT sys_user_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: sys_user sys_user_tenant_id_username_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_tenant_id_username_key UNIQUE (tenant_id, username);


--
-- Name: task_job task_job_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_job
    ADD CONSTRAINT task_job_pkey PRIMARY KEY (id);


--
-- Name: task_node task_node_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_pkey PRIMARY KEY (id);


--
-- Name: task_node task_node_tenant_id_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_tenant_id_code_key UNIQUE (tenant_id, code);


--
-- Name: task_workflow_node_type task_workflow_node_type_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type
    ADD CONSTRAINT task_workflow_node_type_pkey PRIMARY KEY (id);


--
-- Name: task_workflow_node_type task_workflow_node_type_tenant_id_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type
    ADD CONSTRAINT task_workflow_node_type_tenant_id_code_key UNIQUE (tenant_id, code);


--
-- Name: task_workflow task_workflow_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT task_workflow_pkey PRIMARY KEY (id);


--
-- Name: sys_dict_data uq_dict_data_value; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT uq_dict_data_value UNIQUE (tenant_id, dict_type_id, dict_value);


--
-- Name: platform_package_menu uq_package_menu; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package_menu
    ADD CONSTRAINT uq_package_menu UNIQUE (package_id, menu_id);


--
-- Name: platform_package_plugin uq_package_plugin; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package_plugin
    ADD CONSTRAINT uq_package_plugin UNIQUE (package_id, plugin_id);


--
-- Name: task_workflow uq_task_workflow_code; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT uq_task_workflow_code UNIQUE (tenant_id, code);


--
-- Name: platform_tenant_plugin uq_tenant_plugin; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_tenant_plugin
    ADD CONSTRAINT uq_tenant_plugin UNIQUE (tenant_id, plugin_id);


--
-- Name: sys_notice_read uq_user_notice_read; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice_read
    ADD CONSTRAINT uq_user_notice_read PRIMARY KEY (user_id, notice_id);


--
-- Name: platform_user_tenant uq_user_tenant; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_user_tenant
    ADD CONSTRAINT uq_user_tenant UNIQUE (user_id, tenant_id);


--
-- Name: ix_apscheduler_jobs_next_run_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_apscheduler_jobs_next_run_time ON public.apscheduler_jobs USING btree (next_run_time);


--
-- Name: ix_example_demo_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_example_demo_created_id ON public.example_demo USING btree (created_id);


--
-- Name: ix_example_demo_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_example_demo_created_time ON public.example_demo USING btree (created_time);


--
-- Name: ix_example_demo_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_example_demo_deleted_id ON public.example_demo USING btree (deleted_id);


--
-- Name: ix_example_demo_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_example_demo_deleted_time ON public.example_demo USING btree (deleted_time);


--
-- Name: ix_example_demo_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_example_demo_id ON public.example_demo USING btree (id);


--
-- Name: ix_example_demo_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_example_demo_is_deleted ON public.example_demo USING btree (is_deleted);


--
-- Name: ix_example_demo_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_example_demo_status ON public.example_demo USING btree (status);


--
-- Name: ix_example_demo_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_example_demo_tenant_id ON public.example_demo USING btree (tenant_id);


--
-- Name: ix_example_demo_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_example_demo_updated_id ON public.example_demo USING btree (updated_id);


--
-- Name: ix_example_demo_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_example_demo_updated_time ON public.example_demo USING btree (updated_time);


--
-- Name: ix_example_demo_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_example_demo_uuid ON public.example_demo USING btree (uuid);


--
-- Name: ix_gen_table_column_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_created_id ON public.gen_table_column USING btree (created_id);


--
-- Name: ix_gen_table_column_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_created_time ON public.gen_table_column USING btree (created_time);


--
-- Name: ix_gen_table_column_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_deleted_id ON public.gen_table_column USING btree (deleted_id);


--
-- Name: ix_gen_table_column_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_deleted_time ON public.gen_table_column USING btree (deleted_time);


--
-- Name: ix_gen_table_column_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_id ON public.gen_table_column USING btree (id);


--
-- Name: ix_gen_table_column_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_is_deleted ON public.gen_table_column USING btree (is_deleted);


--
-- Name: ix_gen_table_column_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_status ON public.gen_table_column USING btree (status);


--
-- Name: ix_gen_table_column_table_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_table_id ON public.gen_table_column USING btree (table_id);


--
-- Name: ix_gen_table_column_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_tenant_id ON public.gen_table_column USING btree (tenant_id);


--
-- Name: ix_gen_table_column_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_updated_id ON public.gen_table_column USING btree (updated_id);


--
-- Name: ix_gen_table_column_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_updated_time ON public.gen_table_column USING btree (updated_time);


--
-- Name: ix_gen_table_column_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_gen_table_column_uuid ON public.gen_table_column USING btree (uuid);


--
-- Name: ix_gen_table_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_created_id ON public.gen_table USING btree (created_id);


--
-- Name: ix_gen_table_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_created_time ON public.gen_table USING btree (created_time);


--
-- Name: ix_gen_table_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_deleted_id ON public.gen_table USING btree (deleted_id);


--
-- Name: ix_gen_table_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_deleted_time ON public.gen_table USING btree (deleted_time);


--
-- Name: ix_gen_table_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_id ON public.gen_table USING btree (id);


--
-- Name: ix_gen_table_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_is_deleted ON public.gen_table USING btree (is_deleted);


--
-- Name: ix_gen_table_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_status ON public.gen_table USING btree (status);


--
-- Name: ix_gen_table_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_tenant_id ON public.gen_table USING btree (tenant_id);


--
-- Name: ix_gen_table_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_updated_id ON public.gen_table USING btree (updated_id);


--
-- Name: ix_gen_table_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_updated_time ON public.gen_table USING btree (updated_time);


--
-- Name: ix_gen_table_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_gen_table_uuid ON public.gen_table USING btree (uuid);


--
-- Name: ix_platform_email_config_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_config_created_time ON public.platform_email_config USING btree (created_time);


--
-- Name: ix_platform_email_config_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_config_deleted_time ON public.platform_email_config USING btree (deleted_time);


--
-- Name: ix_platform_email_config_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_config_id ON public.platform_email_config USING btree (id);


--
-- Name: ix_platform_email_config_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_config_is_deleted ON public.platform_email_config USING btree (is_deleted);


--
-- Name: ix_platform_email_config_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_config_status ON public.platform_email_config USING btree (status);


--
-- Name: ix_platform_email_config_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_config_updated_time ON public.platform_email_config USING btree (updated_time);


--
-- Name: ix_platform_email_config_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_email_config_uuid ON public.platform_email_config USING btree (uuid);


--
-- Name: ix_platform_email_log_config_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_config_id ON public.platform_email_log USING btree (config_id);


--
-- Name: ix_platform_email_log_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_created_id ON public.platform_email_log USING btree (created_id);


--
-- Name: ix_platform_email_log_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_created_time ON public.platform_email_log USING btree (created_time);


--
-- Name: ix_platform_email_log_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_deleted_id ON public.platform_email_log USING btree (deleted_id);


--
-- Name: ix_platform_email_log_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_deleted_time ON public.platform_email_log USING btree (deleted_time);


--
-- Name: ix_platform_email_log_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_id ON public.platform_email_log USING btree (id);


--
-- Name: ix_platform_email_log_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_is_deleted ON public.platform_email_log USING btree (is_deleted);


--
-- Name: ix_platform_email_log_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_status ON public.platform_email_log USING btree (status);


--
-- Name: ix_platform_email_log_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_tenant_id ON public.platform_email_log USING btree (tenant_id);


--
-- Name: ix_platform_email_log_to_email; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_to_email ON public.platform_email_log USING btree (to_email);


--
-- Name: ix_platform_email_log_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_updated_id ON public.platform_email_log USING btree (updated_id);


--
-- Name: ix_platform_email_log_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_log_updated_time ON public.platform_email_log USING btree (updated_time);


--
-- Name: ix_platform_email_log_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_email_log_uuid ON public.platform_email_log USING btree (uuid);


--
-- Name: ix_platform_email_template_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_template_created_time ON public.platform_email_template USING btree (created_time);


--
-- Name: ix_platform_email_template_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_template_deleted_time ON public.platform_email_template USING btree (deleted_time);


--
-- Name: ix_platform_email_template_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_template_id ON public.platform_email_template USING btree (id);


--
-- Name: ix_platform_email_template_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_template_is_deleted ON public.platform_email_template USING btree (is_deleted);


--
-- Name: ix_platform_email_template_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_template_status ON public.platform_email_template USING btree (status);


--
-- Name: ix_platform_email_template_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_email_template_updated_time ON public.platform_email_template USING btree (updated_time);


--
-- Name: ix_platform_email_template_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_email_template_uuid ON public.platform_email_template USING btree (uuid);


--
-- Name: ix_platform_invoice_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_invoice_created_id ON public.platform_invoice USING btree (created_id);


--
-- Name: ix_platform_invoice_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_invoice_created_time ON public.platform_invoice USING btree (created_time);


--
-- Name: ix_platform_invoice_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_invoice_deleted_id ON public.platform_invoice USING btree (deleted_id);


--
-- Name: ix_platform_invoice_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_invoice_deleted_time ON public.platform_invoice USING btree (deleted_time);


--
-- Name: ix_platform_invoice_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_invoice_id ON public.platform_invoice USING btree (id);


--
-- Name: ix_platform_invoice_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_invoice_is_deleted ON public.platform_invoice USING btree (is_deleted);


--
-- Name: ix_platform_invoice_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_invoice_status ON public.platform_invoice USING btree (status);


--
-- Name: ix_platform_invoice_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_invoice_tenant_id ON public.platform_invoice USING btree (tenant_id);


--
-- Name: ix_platform_invoice_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_invoice_updated_id ON public.platform_invoice USING btree (updated_id);


--
-- Name: ix_platform_invoice_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_invoice_updated_time ON public.platform_invoice USING btree (updated_time);


--
-- Name: ix_platform_invoice_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_invoice_uuid ON public.platform_invoice USING btree (uuid);


--
-- Name: ix_platform_menu_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_menu_created_time ON public.platform_menu USING btree (created_time);


--
-- Name: ix_platform_menu_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_menu_deleted_time ON public.platform_menu USING btree (deleted_time);


--
-- Name: ix_platform_menu_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_menu_id ON public.platform_menu USING btree (id);


--
-- Name: ix_platform_menu_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_menu_is_deleted ON public.platform_menu USING btree (is_deleted);


--
-- Name: ix_platform_menu_parent_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_menu_parent_id ON public.platform_menu USING btree (parent_id);


--
-- Name: ix_platform_menu_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_menu_status ON public.platform_menu USING btree (status);


--
-- Name: ix_platform_menu_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_menu_updated_time ON public.platform_menu USING btree (updated_time);


--
-- Name: ix_platform_menu_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_menu_uuid ON public.platform_menu USING btree (uuid);


--
-- Name: ix_platform_order_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_order_created_time ON public.platform_order USING btree (created_time);


--
-- Name: ix_platform_order_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_order_deleted_time ON public.platform_order USING btree (deleted_time);


--
-- Name: ix_platform_order_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_order_id ON public.platform_order USING btree (id);


--
-- Name: ix_platform_order_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_order_is_deleted ON public.platform_order USING btree (is_deleted);


--
-- Name: ix_platform_order_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_order_status ON public.platform_order USING btree (status);


--
-- Name: ix_platform_order_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_order_tenant_id ON public.platform_order USING btree (tenant_id);


--
-- Name: ix_platform_order_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_order_updated_time ON public.platform_order USING btree (updated_time);


--
-- Name: ix_platform_order_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_order_uuid ON public.platform_order USING btree (uuid);


--
-- Name: ix_platform_package_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_package_created_time ON public.platform_package USING btree (created_time);


--
-- Name: ix_platform_package_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_package_deleted_time ON public.platform_package USING btree (deleted_time);


--
-- Name: ix_platform_package_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_package_id ON public.platform_package USING btree (id);


--
-- Name: ix_platform_package_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_package_is_deleted ON public.platform_package USING btree (is_deleted);


--
-- Name: ix_platform_package_menu_menu_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_package_menu_menu_id ON public.platform_package_menu USING btree (menu_id);


--
-- Name: ix_platform_package_menu_package_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_package_menu_package_id ON public.platform_package_menu USING btree (package_id);


--
-- Name: ix_platform_package_plugin_package_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_package_plugin_package_id ON public.platform_package_plugin USING btree (package_id);


--
-- Name: ix_platform_package_plugin_plugin_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_package_plugin_plugin_id ON public.platform_package_plugin USING btree (plugin_id);


--
-- Name: ix_platform_package_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_package_status ON public.platform_package USING btree (status);


--
-- Name: ix_platform_package_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_package_updated_time ON public.platform_package USING btree (updated_time);


--
-- Name: ix_platform_package_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_package_uuid ON public.platform_package USING btree (uuid);


--
-- Name: ix_platform_payment_record_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_payment_record_created_time ON public.platform_payment_record USING btree (created_time);


--
-- Name: ix_platform_payment_record_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_payment_record_deleted_time ON public.platform_payment_record USING btree (deleted_time);


--
-- Name: ix_platform_payment_record_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_payment_record_id ON public.platform_payment_record USING btree (id);


--
-- Name: ix_platform_payment_record_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_payment_record_is_deleted ON public.platform_payment_record USING btree (is_deleted);


--
-- Name: ix_platform_payment_record_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_payment_record_status ON public.platform_payment_record USING btree (status);


--
-- Name: ix_platform_payment_record_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_payment_record_tenant_id ON public.platform_payment_record USING btree (tenant_id);


--
-- Name: ix_platform_payment_record_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_payment_record_updated_time ON public.platform_payment_record USING btree (updated_time);


--
-- Name: ix_platform_payment_record_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_payment_record_uuid ON public.platform_payment_record USING btree (uuid);


--
-- Name: ix_platform_plugin_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_plugin_created_time ON public.platform_plugin USING btree (created_time);


--
-- Name: ix_platform_plugin_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_plugin_deleted_time ON public.platform_plugin USING btree (deleted_time);


--
-- Name: ix_platform_plugin_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_plugin_id ON public.platform_plugin USING btree (id);


--
-- Name: ix_platform_plugin_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_plugin_is_deleted ON public.platform_plugin USING btree (is_deleted);


--
-- Name: ix_platform_plugin_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_plugin_status ON public.platform_plugin USING btree (status);


--
-- Name: ix_platform_plugin_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_plugin_updated_time ON public.platform_plugin USING btree (updated_time);


--
-- Name: ix_platform_plugin_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_plugin_uuid ON public.platform_plugin USING btree (uuid);


--
-- Name: ix_platform_refund_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_refund_created_time ON public.platform_refund USING btree (created_time);


--
-- Name: ix_platform_refund_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_refund_deleted_time ON public.platform_refund USING btree (deleted_time);


--
-- Name: ix_platform_refund_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_refund_id ON public.platform_refund USING btree (id);


--
-- Name: ix_platform_refund_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_refund_is_deleted ON public.platform_refund USING btree (is_deleted);


--
-- Name: ix_platform_refund_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_refund_status ON public.platform_refund USING btree (status);


--
-- Name: ix_platform_refund_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_refund_tenant_id ON public.platform_refund USING btree (tenant_id);


--
-- Name: ix_platform_refund_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_refund_updated_time ON public.platform_refund USING btree (updated_time);


--
-- Name: ix_platform_refund_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_refund_uuid ON public.platform_refund USING btree (uuid);


--
-- Name: ix_platform_tenant_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_tenant_created_time ON public.platform_tenant USING btree (created_time);


--
-- Name: ix_platform_tenant_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_tenant_deleted_time ON public.platform_tenant USING btree (deleted_time);


--
-- Name: ix_platform_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_tenant_id ON public.platform_tenant USING btree (id);


--
-- Name: ix_platform_tenant_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_tenant_is_deleted ON public.platform_tenant USING btree (is_deleted);


--
-- Name: ix_platform_tenant_package_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_tenant_package_id ON public.platform_tenant USING btree (package_id);


--
-- Name: ix_platform_tenant_plugin_plugin_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_tenant_plugin_plugin_id ON public.platform_tenant_plugin USING btree (plugin_id);


--
-- Name: ix_platform_tenant_plugin_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_tenant_plugin_tenant_id ON public.platform_tenant_plugin USING btree (tenant_id);


--
-- Name: ix_platform_tenant_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_tenant_status ON public.platform_tenant USING btree (status);


--
-- Name: ix_platform_tenant_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_tenant_updated_time ON public.platform_tenant USING btree (updated_time);


--
-- Name: ix_platform_tenant_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_platform_tenant_uuid ON public.platform_tenant USING btree (uuid);


--
-- Name: ix_platform_user_tenant_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_user_tenant_tenant_id ON public.platform_user_tenant USING btree (tenant_id);


--
-- Name: ix_platform_user_tenant_user_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_platform_user_tenant_user_id ON public.platform_user_tenant USING btree (user_id);


--
-- Name: ix_sys_dept_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_created_id ON public.sys_dept USING btree (created_id);


--
-- Name: ix_sys_dept_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_created_time ON public.sys_dept USING btree (created_time);


--
-- Name: ix_sys_dept_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_deleted_id ON public.sys_dept USING btree (deleted_id);


--
-- Name: ix_sys_dept_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_deleted_time ON public.sys_dept USING btree (deleted_time);


--
-- Name: ix_sys_dept_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_id ON public.sys_dept USING btree (id);


--
-- Name: ix_sys_dept_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_is_deleted ON public.sys_dept USING btree (is_deleted);


--
-- Name: ix_sys_dept_parent_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_parent_id ON public.sys_dept USING btree (parent_id);


--
-- Name: ix_sys_dept_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_status ON public.sys_dept USING btree (status);


--
-- Name: ix_sys_dept_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_tenant_id ON public.sys_dept USING btree (tenant_id);


--
-- Name: ix_sys_dept_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_updated_id ON public.sys_dept USING btree (updated_id);


--
-- Name: ix_sys_dept_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_updated_time ON public.sys_dept USING btree (updated_time);


--
-- Name: ix_sys_dept_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_dept_uuid ON public.sys_dept USING btree (uuid);


--
-- Name: ix_sys_dict_data_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_data_created_time ON public.sys_dict_data USING btree (created_time);


--
-- Name: ix_sys_dict_data_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_data_deleted_time ON public.sys_dict_data USING btree (deleted_time);


--
-- Name: ix_sys_dict_data_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_data_id ON public.sys_dict_data USING btree (id);


--
-- Name: ix_sys_dict_data_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_data_is_deleted ON public.sys_dict_data USING btree (is_deleted);


--
-- Name: ix_sys_dict_data_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_data_status ON public.sys_dict_data USING btree (status);


--
-- Name: ix_sys_dict_data_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_data_tenant_id ON public.sys_dict_data USING btree (tenant_id);


--
-- Name: ix_sys_dict_data_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_data_updated_time ON public.sys_dict_data USING btree (updated_time);


--
-- Name: ix_sys_dict_data_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_dict_data_uuid ON public.sys_dict_data USING btree (uuid);


--
-- Name: ix_sys_dict_type_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_type_created_time ON public.sys_dict_type USING btree (created_time);


--
-- Name: ix_sys_dict_type_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_type_deleted_time ON public.sys_dict_type USING btree (deleted_time);


--
-- Name: ix_sys_dict_type_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_type_id ON public.sys_dict_type USING btree (id);


--
-- Name: ix_sys_dict_type_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_type_is_deleted ON public.sys_dict_type USING btree (is_deleted);


--
-- Name: ix_sys_dict_type_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_type_status ON public.sys_dict_type USING btree (status);


--
-- Name: ix_sys_dict_type_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_type_tenant_id ON public.sys_dict_type USING btree (tenant_id);


--
-- Name: ix_sys_dict_type_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_type_updated_time ON public.sys_dict_type USING btree (updated_time);


--
-- Name: ix_sys_dict_type_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_dict_type_uuid ON public.sys_dict_type USING btree (uuid);


--
-- Name: ix_sys_login_log_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_login_log_created_id ON public.sys_login_log USING btree (created_id);


--
-- Name: ix_sys_login_log_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_login_log_created_time ON public.sys_login_log USING btree (created_time);


--
-- Name: ix_sys_login_log_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_login_log_deleted_id ON public.sys_login_log USING btree (deleted_id);


--
-- Name: ix_sys_login_log_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_login_log_deleted_time ON public.sys_login_log USING btree (deleted_time);


--
-- Name: ix_sys_login_log_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_login_log_id ON public.sys_login_log USING btree (id);


--
-- Name: ix_sys_login_log_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_login_log_is_deleted ON public.sys_login_log USING btree (is_deleted);


--
-- Name: ix_sys_login_log_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_login_log_status ON public.sys_login_log USING btree (status);


--
-- Name: ix_sys_login_log_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_login_log_tenant_id ON public.sys_login_log USING btree (tenant_id);


--
-- Name: ix_sys_login_log_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_login_log_updated_id ON public.sys_login_log USING btree (updated_id);


--
-- Name: ix_sys_login_log_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_login_log_updated_time ON public.sys_login_log USING btree (updated_time);


--
-- Name: ix_sys_login_log_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_login_log_uuid ON public.sys_login_log USING btree (uuid);


--
-- Name: ix_sys_notice_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_created_id ON public.sys_notice USING btree (created_id);


--
-- Name: ix_sys_notice_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_created_time ON public.sys_notice USING btree (created_time);


--
-- Name: ix_sys_notice_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_deleted_id ON public.sys_notice USING btree (deleted_id);


--
-- Name: ix_sys_notice_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_deleted_time ON public.sys_notice USING btree (deleted_time);


--
-- Name: ix_sys_notice_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_id ON public.sys_notice USING btree (id);


--
-- Name: ix_sys_notice_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_is_deleted ON public.sys_notice USING btree (is_deleted);


--
-- Name: ix_sys_notice_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_status ON public.sys_notice USING btree (status);


--
-- Name: ix_sys_notice_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_tenant_id ON public.sys_notice USING btree (tenant_id);


--
-- Name: ix_sys_notice_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_updated_id ON public.sys_notice USING btree (updated_id);


--
-- Name: ix_sys_notice_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_updated_time ON public.sys_notice USING btree (updated_time);


--
-- Name: ix_sys_notice_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_notice_uuid ON public.sys_notice USING btree (uuid);


--
-- Name: ix_sys_operation_log_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_operation_log_created_id ON public.sys_operation_log USING btree (created_id);


--
-- Name: ix_sys_operation_log_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_operation_log_created_time ON public.sys_operation_log USING btree (created_time);


--
-- Name: ix_sys_operation_log_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_operation_log_deleted_id ON public.sys_operation_log USING btree (deleted_id);


--
-- Name: ix_sys_operation_log_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_operation_log_deleted_time ON public.sys_operation_log USING btree (deleted_time);


--
-- Name: ix_sys_operation_log_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_operation_log_id ON public.sys_operation_log USING btree (id);


--
-- Name: ix_sys_operation_log_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_operation_log_is_deleted ON public.sys_operation_log USING btree (is_deleted);


--
-- Name: ix_sys_operation_log_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_operation_log_status ON public.sys_operation_log USING btree (status);


--
-- Name: ix_sys_operation_log_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_operation_log_tenant_id ON public.sys_operation_log USING btree (tenant_id);


--
-- Name: ix_sys_operation_log_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_operation_log_updated_id ON public.sys_operation_log USING btree (updated_id);


--
-- Name: ix_sys_operation_log_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_operation_log_updated_time ON public.sys_operation_log USING btree (updated_time);


--
-- Name: ix_sys_operation_log_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_operation_log_uuid ON public.sys_operation_log USING btree (uuid);


--
-- Name: ix_sys_param_config_type; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_config_type ON public.sys_param USING btree (config_type);


--
-- Name: ix_sys_param_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_created_id ON public.sys_param USING btree (created_id);


--
-- Name: ix_sys_param_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_created_time ON public.sys_param USING btree (created_time);


--
-- Name: ix_sys_param_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_deleted_id ON public.sys_param USING btree (deleted_id);


--
-- Name: ix_sys_param_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_deleted_time ON public.sys_param USING btree (deleted_time);


--
-- Name: ix_sys_param_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_id ON public.sys_param USING btree (id);


--
-- Name: ix_sys_param_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_is_deleted ON public.sys_param USING btree (is_deleted);


--
-- Name: ix_sys_param_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_status ON public.sys_param USING btree (status);


--
-- Name: ix_sys_param_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_tenant_id ON public.sys_param USING btree (tenant_id);


--
-- Name: ix_sys_param_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_updated_id ON public.sys_param USING btree (updated_id);


--
-- Name: ix_sys_param_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_updated_time ON public.sys_param USING btree (updated_time);


--
-- Name: ix_sys_param_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_param_uuid ON public.sys_param USING btree (uuid);


--
-- Name: ix_sys_position_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_created_id ON public.sys_position USING btree (created_id);


--
-- Name: ix_sys_position_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_created_time ON public.sys_position USING btree (created_time);


--
-- Name: ix_sys_position_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_deleted_id ON public.sys_position USING btree (deleted_id);


--
-- Name: ix_sys_position_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_deleted_time ON public.sys_position USING btree (deleted_time);


--
-- Name: ix_sys_position_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_id ON public.sys_position USING btree (id);


--
-- Name: ix_sys_position_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_is_deleted ON public.sys_position USING btree (is_deleted);


--
-- Name: ix_sys_position_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_status ON public.sys_position USING btree (status);


--
-- Name: ix_sys_position_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_tenant_id ON public.sys_position USING btree (tenant_id);


--
-- Name: ix_sys_position_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_updated_id ON public.sys_position USING btree (updated_id);


--
-- Name: ix_sys_position_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_updated_time ON public.sys_position USING btree (updated_time);


--
-- Name: ix_sys_position_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_position_uuid ON public.sys_position USING btree (uuid);


--
-- Name: ix_sys_role_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_created_id ON public.sys_role USING btree (created_id);


--
-- Name: ix_sys_role_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_created_time ON public.sys_role USING btree (created_time);


--
-- Name: ix_sys_role_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_deleted_id ON public.sys_role USING btree (deleted_id);


--
-- Name: ix_sys_role_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_deleted_time ON public.sys_role USING btree (deleted_time);


--
-- Name: ix_sys_role_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_id ON public.sys_role USING btree (id);


--
-- Name: ix_sys_role_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_is_deleted ON public.sys_role USING btree (is_deleted);


--
-- Name: ix_sys_role_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_status ON public.sys_role USING btree (status);


--
-- Name: ix_sys_role_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_tenant_id ON public.sys_role USING btree (tenant_id);


--
-- Name: ix_sys_role_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_updated_id ON public.sys_role USING btree (updated_id);


--
-- Name: ix_sys_role_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_updated_time ON public.sys_role USING btree (updated_time);


--
-- Name: ix_sys_role_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_role_uuid ON public.sys_role USING btree (uuid);


--
-- Name: ix_sys_ticket_assigned_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_assigned_id ON public.sys_ticket USING btree (assigned_id);


--
-- Name: ix_sys_ticket_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_created_id ON public.sys_ticket USING btree (created_id);


--
-- Name: ix_sys_ticket_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_created_time ON public.sys_ticket USING btree (created_time);


--
-- Name: ix_sys_ticket_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_deleted_id ON public.sys_ticket USING btree (deleted_id);


--
-- Name: ix_sys_ticket_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_deleted_time ON public.sys_ticket USING btree (deleted_time);


--
-- Name: ix_sys_ticket_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_id ON public.sys_ticket USING btree (id);


--
-- Name: ix_sys_ticket_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_is_deleted ON public.sys_ticket USING btree (is_deleted);


--
-- Name: ix_sys_ticket_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_status ON public.sys_ticket USING btree (status);


--
-- Name: ix_sys_ticket_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_tenant_id ON public.sys_ticket USING btree (tenant_id);


--
-- Name: ix_sys_ticket_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_updated_id ON public.sys_ticket USING btree (updated_id);


--
-- Name: ix_sys_ticket_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_ticket_updated_time ON public.sys_ticket USING btree (updated_time);


--
-- Name: ix_sys_ticket_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_ticket_uuid ON public.sys_ticket USING btree (uuid);


--
-- Name: ix_sys_user_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_created_id ON public.sys_user USING btree (created_id);


--
-- Name: ix_sys_user_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_created_time ON public.sys_user USING btree (created_time);


--
-- Name: ix_sys_user_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_deleted_id ON public.sys_user USING btree (deleted_id);


--
-- Name: ix_sys_user_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_deleted_time ON public.sys_user USING btree (deleted_time);


--
-- Name: ix_sys_user_dept_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_dept_id ON public.sys_user USING btree (dept_id);


--
-- Name: ix_sys_user_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_id ON public.sys_user USING btree (id);


--
-- Name: ix_sys_user_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_is_deleted ON public.sys_user USING btree (is_deleted);


--
-- Name: ix_sys_user_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_status ON public.sys_user USING btree (status);


--
-- Name: ix_sys_user_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_tenant_id ON public.sys_user USING btree (tenant_id);


--
-- Name: ix_sys_user_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_updated_id ON public.sys_user USING btree (updated_id);


--
-- Name: ix_sys_user_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_updated_time ON public.sys_user USING btree (updated_time);


--
-- Name: ix_sys_user_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_user_uuid ON public.sys_user USING btree (uuid);


--
-- Name: ix_task_job_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_job_created_time ON public.task_job USING btree (created_time);


--
-- Name: ix_task_job_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_job_deleted_time ON public.task_job USING btree (deleted_time);


--
-- Name: ix_task_job_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_job_id ON public.task_job USING btree (id);


--
-- Name: ix_task_job_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_job_is_deleted ON public.task_job USING btree (is_deleted);


--
-- Name: ix_task_job_job_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_job_job_id ON public.task_job USING btree (job_id);


--
-- Name: ix_task_job_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_job_status ON public.task_job USING btree (status);


--
-- Name: ix_task_job_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_job_tenant_id ON public.task_job USING btree (tenant_id);


--
-- Name: ix_task_job_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_job_updated_time ON public.task_job USING btree (updated_time);


--
-- Name: ix_task_job_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_task_job_uuid ON public.task_job USING btree (uuid);


--
-- Name: ix_task_node_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_created_id ON public.task_node USING btree (created_id);


--
-- Name: ix_task_node_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_created_time ON public.task_node USING btree (created_time);


--
-- Name: ix_task_node_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_deleted_id ON public.task_node USING btree (deleted_id);


--
-- Name: ix_task_node_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_deleted_time ON public.task_node USING btree (deleted_time);


--
-- Name: ix_task_node_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_id ON public.task_node USING btree (id);


--
-- Name: ix_task_node_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_is_deleted ON public.task_node USING btree (is_deleted);


--
-- Name: ix_task_node_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_status ON public.task_node USING btree (status);


--
-- Name: ix_task_node_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_tenant_id ON public.task_node USING btree (tenant_id);


--
-- Name: ix_task_node_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_updated_id ON public.task_node USING btree (updated_id);


--
-- Name: ix_task_node_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_updated_time ON public.task_node USING btree (updated_time);


--
-- Name: ix_task_node_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_task_node_uuid ON public.task_node USING btree (uuid);


--
-- Name: ix_task_workflow_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_created_id ON public.task_workflow USING btree (created_id);


--
-- Name: ix_task_workflow_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_created_time ON public.task_workflow USING btree (created_time);


--
-- Name: ix_task_workflow_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_deleted_id ON public.task_workflow USING btree (deleted_id);


--
-- Name: ix_task_workflow_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_deleted_time ON public.task_workflow USING btree (deleted_time);


--
-- Name: ix_task_workflow_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_id ON public.task_workflow USING btree (id);


--
-- Name: ix_task_workflow_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_is_deleted ON public.task_workflow USING btree (is_deleted);


--
-- Name: ix_task_workflow_node_type_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_created_id ON public.task_workflow_node_type USING btree (created_id);


--
-- Name: ix_task_workflow_node_type_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_created_time ON public.task_workflow_node_type USING btree (created_time);


--
-- Name: ix_task_workflow_node_type_deleted_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_deleted_id ON public.task_workflow_node_type USING btree (deleted_id);


--
-- Name: ix_task_workflow_node_type_deleted_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_deleted_time ON public.task_workflow_node_type USING btree (deleted_time);


--
-- Name: ix_task_workflow_node_type_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_id ON public.task_workflow_node_type USING btree (id);


--
-- Name: ix_task_workflow_node_type_is_deleted; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_is_deleted ON public.task_workflow_node_type USING btree (is_deleted);


--
-- Name: ix_task_workflow_node_type_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_status ON public.task_workflow_node_type USING btree (status);


--
-- Name: ix_task_workflow_node_type_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_tenant_id ON public.task_workflow_node_type USING btree (tenant_id);


--
-- Name: ix_task_workflow_node_type_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_updated_id ON public.task_workflow_node_type USING btree (updated_id);


--
-- Name: ix_task_workflow_node_type_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_updated_time ON public.task_workflow_node_type USING btree (updated_time);


--
-- Name: ix_task_workflow_node_type_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_task_workflow_node_type_uuid ON public.task_workflow_node_type USING btree (uuid);


--
-- Name: ix_task_workflow_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_status ON public.task_workflow USING btree (status);


--
-- Name: ix_task_workflow_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_tenant_id ON public.task_workflow USING btree (tenant_id);


--
-- Name: ix_task_workflow_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_updated_id ON public.task_workflow USING btree (updated_id);


--
-- Name: ix_task_workflow_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_updated_time ON public.task_workflow USING btree (updated_time);


--
-- Name: ix_task_workflow_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_task_workflow_uuid ON public.task_workflow USING btree (uuid);


--
-- Name: example_demo example_demo_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.example_demo
    ADD CONSTRAINT example_demo_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: example_demo example_demo_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.example_demo
    ADD CONSTRAINT example_demo_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: example_demo example_demo_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.example_demo
    ADD CONSTRAINT example_demo_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: example_demo example_demo_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.example_demo
    ADD CONSTRAINT example_demo_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table_column gen_table_column_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table_column gen_table_column_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table_column gen_table_column_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.gen_table(id) ON DELETE CASCADE;


--
-- Name: gen_table_column gen_table_column_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: gen_table_column gen_table_column_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table gen_table_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table gen_table_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table gen_table_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: gen_table gen_table_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: platform_email_log platform_email_log_config_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_log
    ADD CONSTRAINT platform_email_log_config_id_fkey FOREIGN KEY (config_id) REFERENCES public.platform_email_config(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: platform_email_log platform_email_log_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_log
    ADD CONSTRAINT platform_email_log_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: platform_email_log platform_email_log_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_log
    ADD CONSTRAINT platform_email_log_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: platform_email_log platform_email_log_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_log
    ADD CONSTRAINT platform_email_log_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: platform_email_log platform_email_log_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_email_log
    ADD CONSTRAINT platform_email_log_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: platform_invoice platform_invoice_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_invoice
    ADD CONSTRAINT platform_invoice_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: platform_invoice platform_invoice_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_invoice
    ADD CONSTRAINT platform_invoice_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: platform_invoice platform_invoice_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_invoice
    ADD CONSTRAINT platform_invoice_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.platform_order(id);


--
-- Name: platform_invoice platform_invoice_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_invoice
    ADD CONSTRAINT platform_invoice_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: platform_invoice platform_invoice_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_invoice
    ADD CONSTRAINT platform_invoice_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: platform_menu platform_menu_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_menu
    ADD CONSTRAINT platform_menu_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.platform_menu(id) ON DELETE SET NULL;


--
-- Name: platform_order platform_order_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_order
    ADD CONSTRAINT platform_order_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.platform_package(id);


--
-- Name: platform_order platform_order_plugin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_order
    ADD CONSTRAINT platform_order_plugin_id_fkey FOREIGN KEY (plugin_id) REFERENCES public.platform_plugin(id);


--
-- Name: platform_order platform_order_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_order
    ADD CONSTRAINT platform_order_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: platform_package_menu platform_package_menu_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package_menu
    ADD CONSTRAINT platform_package_menu_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.platform_menu(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: platform_package_menu platform_package_menu_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package_menu
    ADD CONSTRAINT platform_package_menu_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.platform_package(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: platform_package_plugin platform_package_plugin_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package_plugin
    ADD CONSTRAINT platform_package_plugin_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.platform_package(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: platform_package_plugin platform_package_plugin_plugin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_package_plugin
    ADD CONSTRAINT platform_package_plugin_plugin_id_fkey FOREIGN KEY (plugin_id) REFERENCES public.platform_plugin(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: platform_payment_record platform_payment_record_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_payment_record
    ADD CONSTRAINT platform_payment_record_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.platform_order(id);


--
-- Name: platform_payment_record platform_payment_record_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_payment_record
    ADD CONSTRAINT platform_payment_record_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: platform_refund platform_refund_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_refund
    ADD CONSTRAINT platform_refund_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.platform_order(id);


--
-- Name: platform_refund platform_refund_reviewer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_refund
    ADD CONSTRAINT platform_refund_reviewer_id_fkey FOREIGN KEY (reviewer_id) REFERENCES public.sys_user(id);


--
-- Name: platform_refund platform_refund_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_refund
    ADD CONSTRAINT platform_refund_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: platform_tenant platform_tenant_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_tenant
    ADD CONSTRAINT platform_tenant_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.platform_package(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: platform_tenant_plugin platform_tenant_plugin_plugin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_tenant_plugin
    ADD CONSTRAINT platform_tenant_plugin_plugin_id_fkey FOREIGN KEY (plugin_id) REFERENCES public.platform_plugin(id) ON DELETE CASCADE;


--
-- Name: platform_tenant_plugin platform_tenant_plugin_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_tenant_plugin
    ADD CONSTRAINT platform_tenant_plugin_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON DELETE CASCADE;


--
-- Name: platform_user_tenant platform_user_tenant_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_user_tenant
    ADD CONSTRAINT platform_user_tenant_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: platform_user_tenant platform_user_tenant_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.platform_user_tenant
    ADD CONSTRAINT platform_user_tenant_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_dept sys_dept_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dept sys_dept_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dept sys_dept_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.sys_dept(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dept sys_dept_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_dept sys_dept_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dict_data sys_dict_data_dict_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_dict_type_id_fkey FOREIGN KEY (dict_type_id) REFERENCES public.sys_dict_type(id) ON DELETE CASCADE;


--
-- Name: sys_dict_data sys_dict_data_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_dict_type sys_dict_type_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_type
    ADD CONSTRAINT sys_dict_type_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_login_log sys_login_log_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_login_log
    ADD CONSTRAINT sys_login_log_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_login_log sys_login_log_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_login_log
    ADD CONSTRAINT sys_login_log_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_login_log sys_login_log_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_login_log
    ADD CONSTRAINT sys_login_log_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_login_log sys_login_log_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_login_log
    ADD CONSTRAINT sys_login_log_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_notice sys_notice_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_notice sys_notice_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_notice_read sys_notice_read_notice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice_read
    ADD CONSTRAINT sys_notice_read_notice_id_fkey FOREIGN KEY (notice_id) REFERENCES public.sys_notice(id) ON DELETE CASCADE;


--
-- Name: sys_notice_read sys_notice_read_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice_read
    ADD CONSTRAINT sys_notice_read_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.sys_user(id) ON DELETE CASCADE;


--
-- Name: sys_notice sys_notice_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_notice sys_notice_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_operation_log sys_operation_log_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_operation_log
    ADD CONSTRAINT sys_operation_log_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_operation_log sys_operation_log_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_operation_log
    ADD CONSTRAINT sys_operation_log_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_operation_log sys_operation_log_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_operation_log
    ADD CONSTRAINT sys_operation_log_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_operation_log sys_operation_log_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_operation_log
    ADD CONSTRAINT sys_operation_log_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_param sys_param_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_param
    ADD CONSTRAINT sys_param_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_param sys_param_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_param
    ADD CONSTRAINT sys_param_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_param sys_param_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_param
    ADD CONSTRAINT sys_param_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_param sys_param_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_param
    ADD CONSTRAINT sys_param_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_position sys_position_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_position sys_position_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_position sys_position_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_position sys_position_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_role sys_role_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role
    ADD CONSTRAINT sys_role_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_role sys_role_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role
    ADD CONSTRAINT sys_role_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_role_depts sys_role_depts_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role_depts
    ADD CONSTRAINT sys_role_depts_dept_id_fkey FOREIGN KEY (dept_id) REFERENCES public.sys_dept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role_depts sys_role_depts_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role_depts
    ADD CONSTRAINT sys_role_depts_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.sys_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role_menus sys_role_menus_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role_menus
    ADD CONSTRAINT sys_role_menus_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.platform_menu(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role_menus sys_role_menus_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role_menus
    ADD CONSTRAINT sys_role_menus_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.sys_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role sys_role_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role
    ADD CONSTRAINT sys_role_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_role sys_role_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role
    ADD CONSTRAINT sys_role_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_ticket sys_ticket_assigned_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_ticket
    ADD CONSTRAINT sys_ticket_assigned_id_fkey FOREIGN KEY (assigned_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_ticket sys_ticket_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_ticket
    ADD CONSTRAINT sys_ticket_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_ticket sys_ticket_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_ticket
    ADD CONSTRAINT sys_ticket_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_ticket sys_ticket_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_ticket
    ADD CONSTRAINT sys_ticket_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_ticket sys_ticket_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_ticket
    ADD CONSTRAINT sys_ticket_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_user sys_user_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_user sys_user_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_user sys_user_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_dept_id_fkey FOREIGN KEY (dept_id) REFERENCES public.sys_dept(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_user_positions sys_user_positions_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user_positions
    ADD CONSTRAINT sys_user_positions_position_id_fkey FOREIGN KEY (position_id) REFERENCES public.sys_position(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user_positions sys_user_positions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user_positions
    ADD CONSTRAINT sys_user_positions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user_roles sys_user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user_roles
    ADD CONSTRAINT sys_user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.sys_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user_roles sys_user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user_roles
    ADD CONSTRAINT sys_user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user sys_user_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sys_user sys_user_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_job task_job_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_job
    ADD CONSTRAINT task_job_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: task_node task_node_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_node task_node_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_node task_node_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: task_node task_node_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_workflow task_workflow_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT task_workflow_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_workflow task_workflow_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT task_workflow_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_workflow_node_type task_workflow_node_type_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type
    ADD CONSTRAINT task_workflow_node_type_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_workflow_node_type task_workflow_node_type_deleted_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type
    ADD CONSTRAINT task_workflow_node_type_deleted_id_fkey FOREIGN KEY (deleted_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_workflow_node_type task_workflow_node_type_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type
    ADD CONSTRAINT task_workflow_node_type_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: task_workflow_node_type task_workflow_node_type_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type
    ADD CONSTRAINT task_workflow_node_type_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_workflow task_workflow_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT task_workflow_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.platform_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: task_workflow task_workflow_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT task_workflow_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

\unrestrict qwiwcp7I4gdDmIy1kyj9QBOQCzllutf9XAPaoJPcYOFGDJwS41ngMgrWMeUHoPW

