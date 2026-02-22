--
-- PostgreSQL database dump
--

\restrict ulNIgdx7CtT5MrgK5O5igyKTPSLK56cbbdePKwjuQbUm20ekyjOAhWcXtSxiDc6

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ai_chat_message; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.ai_chat_message (
    session_id integer NOT NULL,
    type character varying(20) NOT NULL,
    content text NOT NULL,
    "timestamp" integer NOT NULL,
    files json,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.ai_chat_message OWNER TO tao;

--
-- Name: TABLE ai_chat_message; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.ai_chat_message IS '聊天消息表';


--
-- Name: COLUMN ai_chat_message.session_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message.session_id IS '会话ID';


--
-- Name: COLUMN ai_chat_message.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message.type IS '消息类型: user/assistant';


--
-- Name: COLUMN ai_chat_message.content; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message.content IS '消息内容';


--
-- Name: COLUMN ai_chat_message."timestamp"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message."timestamp" IS '时间戳';


--
-- Name: COLUMN ai_chat_message.files; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message.files IS '关联的文件信息';


--
-- Name: COLUMN ai_chat_message.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message.id IS '主键ID';


--
-- Name: COLUMN ai_chat_message.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN ai_chat_message.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN ai_chat_message.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message.description IS '备注/描述';


--
-- Name: COLUMN ai_chat_message.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message.created_time IS '创建时间';


--
-- Name: COLUMN ai_chat_message.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_message.updated_time IS '更新时间';


--
-- Name: ai_chat_message_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.ai_chat_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_chat_message_id_seq OWNER TO tao;

--
-- Name: ai_chat_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.ai_chat_message_id_seq OWNED BY public.ai_chat_message.id;


--
-- Name: ai_chat_session; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.ai_chat_session (
    title character varying(200) NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.ai_chat_session OWNER TO tao;

--
-- Name: TABLE ai_chat_session; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.ai_chat_session IS '聊天会话表';


--
-- Name: COLUMN ai_chat_session.title; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_session.title IS '会话标题';


--
-- Name: COLUMN ai_chat_session.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_session.id IS '主键ID';


--
-- Name: COLUMN ai_chat_session.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_session.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN ai_chat_session.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_session.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN ai_chat_session.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_session.description IS '备注/描述';


--
-- Name: COLUMN ai_chat_session.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_session.created_time IS '创建时间';


--
-- Name: COLUMN ai_chat_session.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_session.updated_time IS '更新时间';


--
-- Name: COLUMN ai_chat_session.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_session.created_id IS '创建人ID';


--
-- Name: COLUMN ai_chat_session.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_chat_session.updated_id IS '更新人ID';


--
-- Name: ai_chat_session_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.ai_chat_session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_chat_session_id_seq OWNER TO tao;

--
-- Name: ai_chat_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.ai_chat_session_id_seq OWNED BY public.ai_chat_session.id;


--
-- Name: app_myapp; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.app_myapp (
    name character varying(64) NOT NULL,
    access_url character varying(500) NOT NULL,
    icon_url character varying(300),
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.app_myapp OWNER TO tao;

--
-- Name: TABLE app_myapp; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.app_myapp IS '应用系统表';


--
-- Name: COLUMN app_myapp.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.name IS '应用名称';


--
-- Name: COLUMN app_myapp.access_url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.access_url IS '访问地址';


--
-- Name: COLUMN app_myapp.icon_url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.icon_url IS '应用图标URL';


--
-- Name: COLUMN app_myapp.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.id IS '主键ID';


--
-- Name: COLUMN app_myapp.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN app_myapp.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN app_myapp.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.description IS '备注/描述';


--
-- Name: COLUMN app_myapp.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.created_time IS '创建时间';


--
-- Name: COLUMN app_myapp.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.updated_time IS '更新时间';


--
-- Name: COLUMN app_myapp.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.created_id IS '创建人ID';


--
-- Name: COLUMN app_myapp.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.updated_id IS '更新人ID';


--
-- Name: app_myapp_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.app_myapp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.app_myapp_id_seq OWNER TO tao;

--
-- Name: app_myapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.app_myapp_id_seq OWNED BY public.app_myapp.id;


--
-- Name: apscheduler_jobs; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.apscheduler_jobs (
    id character varying(191) NOT NULL,
    next_run_time double precision,
    job_state bytea NOT NULL
);


ALTER TABLE public.apscheduler_jobs OWNER TO tao;

--
-- Name: gen_demo; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.gen_demo (
    name character varying(64) NOT NULL,
    a integer,
    b bigint,
    c double precision,
    d boolean NOT NULL,
    e date,
    f time without time zone,
    g timestamp without time zone,
    h text,
    i json,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.gen_demo OWNER TO tao;

--
-- Name: TABLE gen_demo; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.gen_demo IS '示例表';


--
-- Name: COLUMN gen_demo.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.name IS '名称';


--
-- Name: COLUMN gen_demo.a; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.a IS '整数';


--
-- Name: COLUMN gen_demo.b; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.b IS '大整数';


--
-- Name: COLUMN gen_demo.c; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.c IS '浮点数';


--
-- Name: COLUMN gen_demo.d; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.d IS '布尔型';


--
-- Name: COLUMN gen_demo.e; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.e IS '日期';


--
-- Name: COLUMN gen_demo.f; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.f IS '时间';


--
-- Name: COLUMN gen_demo.g; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.g IS '日期时间';


--
-- Name: COLUMN gen_demo.h; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.h IS '长文本';


--
-- Name: COLUMN gen_demo.i; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.i IS '元数据(JSON格式)';


--
-- Name: COLUMN gen_demo.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.id IS '主键ID';


--
-- Name: COLUMN gen_demo.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_demo.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN gen_demo.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.description IS '备注/描述';


--
-- Name: COLUMN gen_demo.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.created_time IS '创建时间';


--
-- Name: COLUMN gen_demo.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.updated_time IS '更新时间';


--
-- Name: COLUMN gen_demo.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.created_id IS '创建人ID';


--
-- Name: COLUMN gen_demo.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.updated_id IS '更新人ID';


--
-- Name: gen_demo_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.gen_demo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_demo_id_seq OWNER TO tao;

--
-- Name: gen_demo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.gen_demo_id_seq OWNED BY public.gen_demo.id;


--
-- Name: gen_table; Type: TABLE; Schema: public; Owner: tao
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
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.gen_table OWNER TO tao;

--
-- Name: TABLE gen_table; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.gen_table IS '代码生成表';


--
-- Name: COLUMN gen_table.table_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.table_name IS '表名称';


--
-- Name: COLUMN gen_table.table_comment; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.table_comment IS '表描述';


--
-- Name: COLUMN gen_table.class_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.class_name IS '实体类名称';


--
-- Name: COLUMN gen_table.package_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.package_name IS '生成包路径';


--
-- Name: COLUMN gen_table.module_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.module_name IS '生成模块名';


--
-- Name: COLUMN gen_table.business_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.business_name IS '生成业务名';


--
-- Name: COLUMN gen_table.function_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.function_name IS '生成功能名';


--
-- Name: COLUMN gen_table.sub_table_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.sub_table_name IS '关联子表的表名';


--
-- Name: COLUMN gen_table.sub_table_fk_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.sub_table_fk_name IS '子表关联的外键名';


--
-- Name: COLUMN gen_table.parent_menu_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.parent_menu_id IS '父菜单ID';


--
-- Name: COLUMN gen_table.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.id IS '主键ID';


--
-- Name: COLUMN gen_table.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_table.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN gen_table.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.description IS '备注/描述';


--
-- Name: COLUMN gen_table.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.created_time IS '创建时间';


--
-- Name: COLUMN gen_table.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.updated_time IS '更新时间';


--
-- Name: COLUMN gen_table.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.created_id IS '创建人ID';


--
-- Name: COLUMN gen_table.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.updated_id IS '更新人ID';


--
-- Name: gen_table_column; Type: TABLE; Schema: public; Owner: tao
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
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.gen_table_column OWNER TO tao;

--
-- Name: TABLE gen_table_column; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.gen_table_column IS '代码生成表字段';


--
-- Name: COLUMN gen_table_column.column_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_name IS '列名称';


--
-- Name: COLUMN gen_table_column.column_comment; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_comment IS '列描述';


--
-- Name: COLUMN gen_table_column.column_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_type IS '列类型';


--
-- Name: COLUMN gen_table_column.column_length; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_length IS '列长度';


--
-- Name: COLUMN gen_table_column.column_default; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_default IS '列默认值';


--
-- Name: COLUMN gen_table_column.is_pk; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_pk IS '是否主键';


--
-- Name: COLUMN gen_table_column.is_increment; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_increment IS '是否自增';


--
-- Name: COLUMN gen_table_column.is_nullable; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_nullable IS '是否允许为空';


--
-- Name: COLUMN gen_table_column.is_unique; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_unique IS '是否唯一';


--
-- Name: COLUMN gen_table_column.python_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.python_type IS 'Python类型';


--
-- Name: COLUMN gen_table_column.python_field; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.python_field IS 'Python字段名';


--
-- Name: COLUMN gen_table_column.is_insert; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_insert IS '是否为新增字段';


--
-- Name: COLUMN gen_table_column.is_edit; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_edit IS '是否编辑字段';


--
-- Name: COLUMN gen_table_column.is_list; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_list IS '是否列表字段';


--
-- Name: COLUMN gen_table_column.is_query; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_query IS '是否查询字段';


--
-- Name: COLUMN gen_table_column.query_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.query_type IS '查询方式';


--
-- Name: COLUMN gen_table_column.html_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.html_type IS '显示类型';


--
-- Name: COLUMN gen_table_column.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.dict_type IS '字典类型';


--
-- Name: COLUMN gen_table_column.sort; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.sort IS '排序';


--
-- Name: COLUMN gen_table_column.table_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.table_id IS '归属表编号';


--
-- Name: COLUMN gen_table_column.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.id IS '主键ID';


--
-- Name: COLUMN gen_table_column.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_table_column.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN gen_table_column.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.description IS '备注/描述';


--
-- Name: COLUMN gen_table_column.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.created_time IS '创建时间';


--
-- Name: COLUMN gen_table_column.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.updated_time IS '更新时间';


--
-- Name: COLUMN gen_table_column.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.created_id IS '创建人ID';


--
-- Name: COLUMN gen_table_column.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.updated_id IS '更新人ID';


--
-- Name: gen_table_column_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.gen_table_column_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_table_column_id_seq OWNER TO tao;

--
-- Name: gen_table_column_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.gen_table_column_id_seq OWNED BY public.gen_table_column.id;


--
-- Name: gen_table_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.gen_table_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_table_id_seq OWNER TO tao;

--
-- Name: gen_table_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.gen_table_id_seq OWNED BY public.gen_table.id;


--
-- Name: sys_dept; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_dept (
    name character varying(64) NOT NULL,
    "order" integer NOT NULL,
    code character varying(16),
    leader character varying(32),
    phone character varying(11),
    email character varying(64),
    parent_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_dept OWNER TO tao;

--
-- Name: TABLE sys_dept; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_dept IS '部门表';


--
-- Name: COLUMN sys_dept.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.name IS '部门名称';


--
-- Name: COLUMN sys_dept."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept."order" IS '显示排序';


--
-- Name: COLUMN sys_dept.code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.code IS '部门编码';


--
-- Name: COLUMN sys_dept.leader; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.leader IS '部门负责人';


--
-- Name: COLUMN sys_dept.phone; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.phone IS '手机';


--
-- Name: COLUMN sys_dept.email; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.email IS '邮箱';


--
-- Name: COLUMN sys_dept.parent_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.parent_id IS '父级部门ID';


--
-- Name: COLUMN sys_dept.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.id IS '主键ID';


--
-- Name: COLUMN sys_dept.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_dept.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_dept.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.description IS '备注/描述';


--
-- Name: COLUMN sys_dept.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.created_time IS '创建时间';


--
-- Name: COLUMN sys_dept.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.updated_time IS '更新时间';


--
-- Name: sys_dept_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_dept_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_dept_id_seq OWNER TO tao;

--
-- Name: sys_dept_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_dept_id_seq OWNED BY public.sys_dept.id;


--
-- Name: sys_dict_data; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_dict_data (
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
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_dict_data OWNER TO tao;

--
-- Name: TABLE sys_dict_data; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_dict_data IS '字典数据表';


--
-- Name: COLUMN sys_dict_data.dict_sort; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.dict_sort IS '字典排序';


--
-- Name: COLUMN sys_dict_data.dict_label; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.dict_label IS '字典标签';


--
-- Name: COLUMN sys_dict_data.dict_value; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.dict_value IS '字典键值';


--
-- Name: COLUMN sys_dict_data.css_class; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.css_class IS '样式属性（其他样式扩展）';


--
-- Name: COLUMN sys_dict_data.list_class; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.list_class IS '表格回显样式';


--
-- Name: COLUMN sys_dict_data.is_default; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.is_default IS '是否默认（True是 False否）';


--
-- Name: COLUMN sys_dict_data.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.dict_type IS '字典类型';


--
-- Name: COLUMN sys_dict_data.dict_type_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.dict_type_id IS '字典类型ID';


--
-- Name: COLUMN sys_dict_data.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.id IS '主键ID';


--
-- Name: COLUMN sys_dict_data.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_dict_data.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_dict_data.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.description IS '备注/描述';


--
-- Name: COLUMN sys_dict_data.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.created_time IS '创建时间';


--
-- Name: COLUMN sys_dict_data.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.updated_time IS '更新时间';


--
-- Name: sys_dict_data_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_dict_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_dict_data_id_seq OWNER TO tao;

--
-- Name: sys_dict_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_dict_data_id_seq OWNED BY public.sys_dict_data.id;


--
-- Name: sys_dict_type; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_dict_type (
    dict_name character varying(64) NOT NULL,
    dict_type character varying(255) NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_dict_type OWNER TO tao;

--
-- Name: TABLE sys_dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_dict_type IS '字典类型表';


--
-- Name: COLUMN sys_dict_type.dict_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.dict_name IS '字典名称';


--
-- Name: COLUMN sys_dict_type.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.dict_type IS '字典类型';


--
-- Name: COLUMN sys_dict_type.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.id IS '主键ID';


--
-- Name: COLUMN sys_dict_type.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_dict_type.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_dict_type.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.description IS '备注/描述';


--
-- Name: COLUMN sys_dict_type.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.created_time IS '创建时间';


--
-- Name: COLUMN sys_dict_type.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.updated_time IS '更新时间';


--
-- Name: sys_dict_type_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_dict_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_dict_type_id_seq OWNER TO tao;

--
-- Name: sys_dict_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_dict_type_id_seq OWNED BY public.sys_dict_type.id;


--
-- Name: sys_log; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_log (
    type integer NOT NULL,
    request_path character varying(255) NOT NULL,
    request_method character varying(10) NOT NULL,
    request_payload text,
    request_ip character varying(50),
    login_location character varying(255),
    request_os character varying(64),
    request_browser character varying(64),
    response_code integer NOT NULL,
    response_json text,
    process_time character varying(20),
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.sys_log OWNER TO tao;

--
-- Name: TABLE sys_log; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_log IS '系统日志表';


--
-- Name: COLUMN sys_log.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.type IS '日志类型(1登录日志 2操作日志)';


--
-- Name: COLUMN sys_log.request_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_path IS '请求路径';


--
-- Name: COLUMN sys_log.request_method; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_method IS '请求方式';


--
-- Name: COLUMN sys_log.request_payload; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_payload IS '请求体';


--
-- Name: COLUMN sys_log.request_ip; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_ip IS '请求IP地址';


--
-- Name: COLUMN sys_log.login_location; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.login_location IS '登录位置';


--
-- Name: COLUMN sys_log.request_os; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_os IS '操作系统';


--
-- Name: COLUMN sys_log.request_browser; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_browser IS '浏览器';


--
-- Name: COLUMN sys_log.response_code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.response_code IS '响应状态码';


--
-- Name: COLUMN sys_log.response_json; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.response_json IS '响应体';


--
-- Name: COLUMN sys_log.process_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.process_time IS '处理时间';


--
-- Name: COLUMN sys_log.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.id IS '主键ID';


--
-- Name: COLUMN sys_log.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_log.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_log.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.description IS '备注/描述';


--
-- Name: COLUMN sys_log.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.created_time IS '创建时间';


--
-- Name: COLUMN sys_log.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.updated_time IS '更新时间';


--
-- Name: COLUMN sys_log.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.created_id IS '创建人ID';


--
-- Name: COLUMN sys_log.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.updated_id IS '更新人ID';


--
-- Name: sys_log_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_log_id_seq OWNER TO tao;

--
-- Name: sys_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_log_id_seq OWNED BY public.sys_log.id;


--
-- Name: sys_menu; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_menu (
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
    parent_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_menu OWNER TO tao;

--
-- Name: TABLE sys_menu; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_menu IS '菜单表';


--
-- Name: COLUMN sys_menu.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.name IS '菜单名称';


--
-- Name: COLUMN sys_menu.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.type IS '菜单类型(1:目录 2:菜单 3:按钮/权限 4:链接)';


--
-- Name: COLUMN sys_menu."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu."order" IS '显示排序';


--
-- Name: COLUMN sys_menu.permission; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.permission IS '权限标识(如:module_system:user:query)';


--
-- Name: COLUMN sys_menu.icon; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.icon IS '菜单图标';


--
-- Name: COLUMN sys_menu.route_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.route_name IS '路由名称';


--
-- Name: COLUMN sys_menu.route_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.route_path IS '路由路径';


--
-- Name: COLUMN sys_menu.component_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.component_path IS '组件路径';


--
-- Name: COLUMN sys_menu.redirect; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.redirect IS '重定向地址';


--
-- Name: COLUMN sys_menu.hidden; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.hidden IS '是否隐藏(True:隐藏 False:显示)';


--
-- Name: COLUMN sys_menu.keep_alive; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.keep_alive IS '是否缓存(True:是 False:否)';


--
-- Name: COLUMN sys_menu.always_show; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.always_show IS '是否始终显示(True:是 False:否)';


--
-- Name: COLUMN sys_menu.title; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.title IS '菜单标题';


--
-- Name: COLUMN sys_menu.params; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.params IS '路由参数(JSON对象)';


--
-- Name: COLUMN sys_menu.affix; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.affix IS '是否固定标签页(True:是 False:否)';


--
-- Name: COLUMN sys_menu.parent_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.parent_id IS '父菜单ID';


--
-- Name: COLUMN sys_menu.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.id IS '主键ID';


--
-- Name: COLUMN sys_menu.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_menu.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_menu.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.description IS '备注/描述';


--
-- Name: COLUMN sys_menu.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.created_time IS '创建时间';


--
-- Name: COLUMN sys_menu.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.updated_time IS '更新时间';


--
-- Name: sys_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_menu_id_seq OWNER TO tao;

--
-- Name: sys_menu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_menu_id_seq OWNED BY public.sys_menu.id;


--
-- Name: sys_notice; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_notice (
    notice_title character varying(64) NOT NULL,
    notice_type character varying(1) NOT NULL,
    notice_content text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.sys_notice OWNER TO tao;

--
-- Name: TABLE sys_notice; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_notice IS '通知公告表';


--
-- Name: COLUMN sys_notice.notice_title; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.notice_title IS '公告标题';


--
-- Name: COLUMN sys_notice.notice_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.notice_type IS '公告类型(1通知 2公告)';


--
-- Name: COLUMN sys_notice.notice_content; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.notice_content IS '公告内容';


--
-- Name: COLUMN sys_notice.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.id IS '主键ID';


--
-- Name: COLUMN sys_notice.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_notice.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_notice.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.description IS '备注/描述';


--
-- Name: COLUMN sys_notice.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.created_time IS '创建时间';


--
-- Name: COLUMN sys_notice.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.updated_time IS '更新时间';


--
-- Name: COLUMN sys_notice.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.created_id IS '创建人ID';


--
-- Name: COLUMN sys_notice.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.updated_id IS '更新人ID';


--
-- Name: sys_notice_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_notice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_notice_id_seq OWNER TO tao;

--
-- Name: sys_notice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_notice_id_seq OWNED BY public.sys_notice.id;


--
-- Name: sys_param; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_param (
    config_name character varying(64) NOT NULL,
    config_key character varying(500) NOT NULL,
    config_value character varying(500),
    config_type boolean,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_param OWNER TO tao;

--
-- Name: TABLE sys_param; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_param IS '系统参数表';


--
-- Name: COLUMN sys_param.config_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.config_name IS '参数名称';


--
-- Name: COLUMN sys_param.config_key; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.config_key IS '参数键名';


--
-- Name: COLUMN sys_param.config_value; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.config_value IS '参数键值';


--
-- Name: COLUMN sys_param.config_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.config_type IS '系统内置(True:是 False:否)';


--
-- Name: COLUMN sys_param.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.id IS '主键ID';


--
-- Name: COLUMN sys_param.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_param.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_param.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.description IS '备注/描述';


--
-- Name: COLUMN sys_param.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.created_time IS '创建时间';


--
-- Name: COLUMN sys_param.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.updated_time IS '更新时间';


--
-- Name: sys_param_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_param_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_param_id_seq OWNER TO tao;

--
-- Name: sys_param_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_param_id_seq OWNED BY public.sys_param.id;


--
-- Name: sys_position; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_position (
    name character varying(64) NOT NULL,
    "order" integer NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.sys_position OWNER TO tao;

--
-- Name: TABLE sys_position; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_position IS '岗位表';


--
-- Name: COLUMN sys_position.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.name IS '岗位名称';


--
-- Name: COLUMN sys_position."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position."order" IS '显示排序';


--
-- Name: COLUMN sys_position.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.id IS '主键ID';


--
-- Name: COLUMN sys_position.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_position.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_position.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.description IS '备注/描述';


--
-- Name: COLUMN sys_position.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.created_time IS '创建时间';


--
-- Name: COLUMN sys_position.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.updated_time IS '更新时间';


--
-- Name: COLUMN sys_position.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.created_id IS '创建人ID';


--
-- Name: COLUMN sys_position.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.updated_id IS '更新人ID';


--
-- Name: sys_position_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_position_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_position_id_seq OWNER TO tao;

--
-- Name: sys_position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_position_id_seq OWNED BY public.sys_position.id;


--
-- Name: sys_role; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_role (
    name character varying(64) NOT NULL,
    code character varying(16),
    "order" integer NOT NULL,
    data_scope integer NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_role OWNER TO tao;

--
-- Name: TABLE sys_role; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_role IS '角色表';


--
-- Name: COLUMN sys_role.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.name IS '角色名称';


--
-- Name: COLUMN sys_role.code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.code IS '角色编码';


--
-- Name: COLUMN sys_role."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role."order" IS '显示排序';


--
-- Name: COLUMN sys_role.data_scope; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.data_scope IS '数据权限范围(1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义)';


--
-- Name: COLUMN sys_role.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.id IS '主键ID';


--
-- Name: COLUMN sys_role.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_role.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_role.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.description IS '备注/描述';


--
-- Name: COLUMN sys_role.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.created_time IS '创建时间';


--
-- Name: COLUMN sys_role.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.updated_time IS '更新时间';


--
-- Name: sys_role_depts; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_role_depts (
    role_id integer NOT NULL,
    dept_id integer NOT NULL
);


ALTER TABLE public.sys_role_depts OWNER TO tao;

--
-- Name: TABLE sys_role_depts; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_role_depts IS '角色部门关联表';


--
-- Name: COLUMN sys_role_depts.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role_depts.role_id IS '角色ID';


--
-- Name: COLUMN sys_role_depts.dept_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role_depts.dept_id IS '部门ID';


--
-- Name: sys_role_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_role_id_seq OWNER TO tao;

--
-- Name: sys_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_role_id_seq OWNED BY public.sys_role.id;


--
-- Name: sys_role_menus; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_role_menus (
    role_id integer NOT NULL,
    menu_id integer NOT NULL
);


ALTER TABLE public.sys_role_menus OWNER TO tao;

--
-- Name: TABLE sys_role_menus; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_role_menus IS '角色菜单关联表';


--
-- Name: COLUMN sys_role_menus.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role_menus.role_id IS '角色ID';


--
-- Name: COLUMN sys_role_menus.menu_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role_menus.menu_id IS '菜单ID';


--
-- Name: sys_user; Type: TABLE; Schema: public; Owner: tao
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
    dept_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.sys_user OWNER TO tao;

--
-- Name: TABLE sys_user; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_user IS '用户表';


--
-- Name: COLUMN sys_user.username; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.username IS '用户名/登录账号';


--
-- Name: COLUMN sys_user.password; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.password IS '密码哈希';


--
-- Name: COLUMN sys_user.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.name IS '昵称';


--
-- Name: COLUMN sys_user.mobile; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.mobile IS '手机号';


--
-- Name: COLUMN sys_user.email; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.email IS '邮箱';


--
-- Name: COLUMN sys_user.gender; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.gender IS '性别(0:男 1:女 2:未知)';


--
-- Name: COLUMN sys_user.avatar; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.avatar IS '头像URL地址';


--
-- Name: COLUMN sys_user.is_superuser; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.is_superuser IS '是否超管';


--
-- Name: COLUMN sys_user.last_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.last_login IS '最后登录时间';


--
-- Name: COLUMN sys_user.gitee_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.gitee_login IS 'Gitee登录';


--
-- Name: COLUMN sys_user.github_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.github_login IS 'Github登录';


--
-- Name: COLUMN sys_user.wx_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.wx_login IS '微信登录';


--
-- Name: COLUMN sys_user.qq_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.qq_login IS 'QQ登录';


--
-- Name: COLUMN sys_user.dept_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.dept_id IS '部门ID';


--
-- Name: COLUMN sys_user.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.id IS '主键ID';


--
-- Name: COLUMN sys_user.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_user.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_user.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.description IS '备注/描述';


--
-- Name: COLUMN sys_user.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.created_time IS '创建时间';


--
-- Name: COLUMN sys_user.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.updated_time IS '更新时间';


--
-- Name: COLUMN sys_user.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.created_id IS '创建人ID';


--
-- Name: COLUMN sys_user.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.updated_id IS '更新人ID';


--
-- Name: sys_user_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_user_id_seq OWNER TO tao;

--
-- Name: sys_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_user_id_seq OWNED BY public.sys_user.id;


--
-- Name: sys_user_positions; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_user_positions (
    user_id integer NOT NULL,
    position_id integer NOT NULL
);


ALTER TABLE public.sys_user_positions OWNER TO tao;

--
-- Name: TABLE sys_user_positions; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_user_positions IS '用户岗位关联表';


--
-- Name: COLUMN sys_user_positions.user_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user_positions.user_id IS '用户ID';


--
-- Name: COLUMN sys_user_positions.position_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user_positions.position_id IS '岗位ID';


--
-- Name: sys_user_roles; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_user_roles (
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.sys_user_roles OWNER TO tao;

--
-- Name: TABLE sys_user_roles; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_user_roles IS '用户角色关联表';


--
-- Name: COLUMN sys_user_roles.user_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user_roles.user_id IS '用户ID';


--
-- Name: COLUMN sys_user_roles.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user_roles.role_id IS '角色ID';


--
-- Name: task_job; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.task_job (
    job_id character varying(64) NOT NULL,
    job_name character varying(128),
    trigger_type character varying(32),
    status character varying(16) NOT NULL,
    next_run_time character varying(64),
    job_state text,
    result text,
    error text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.task_job OWNER TO tao;

--
-- Name: TABLE task_job; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.task_job IS '任务执行日志表';


--
-- Name: COLUMN task_job.job_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.job_id IS '任务ID';


--
-- Name: COLUMN task_job.job_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.job_name IS '任务名称';


--
-- Name: COLUMN task_job.trigger_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.trigger_type IS '触发方式: cron/interval/date/manual';


--
-- Name: COLUMN task_job.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.status IS '执行状态';


--
-- Name: COLUMN task_job.next_run_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.next_run_time IS '下次执行时间';


--
-- Name: COLUMN task_job.job_state; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.job_state IS '任务状态信息';


--
-- Name: COLUMN task_job.result; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.result IS '执行结果';


--
-- Name: COLUMN task_job.error; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.error IS '错误信息';


--
-- Name: COLUMN task_job.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.id IS '主键ID';


--
-- Name: COLUMN task_job.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_job.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.description IS '备注/描述';


--
-- Name: COLUMN task_job.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.created_time IS '创建时间';


--
-- Name: COLUMN task_job.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_job.updated_time IS '更新时间';


--
-- Name: task_job_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.task_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_job_id_seq OWNER TO tao;

--
-- Name: task_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.task_job_id_seq OWNED BY public.task_job.id;


--
-- Name: task_node; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.task_node (
    name character varying(64) NOT NULL,
    code character varying(32) NOT NULL,
    category character varying(32) NOT NULL,
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
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.task_node OWNER TO tao;

--
-- Name: TABLE task_node; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.task_node IS '节点类型表';


--
-- Name: COLUMN task_node.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.name IS '节点名称';


--
-- Name: COLUMN task_node.code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.code IS '节点编码';


--
-- Name: COLUMN task_node.category; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.category IS '节点分类';


--
-- Name: COLUMN task_node.jobstore; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.jobstore IS '存储器';


--
-- Name: COLUMN task_node.executor; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.executor IS '执行器';


--
-- Name: COLUMN task_node.trigger; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.trigger IS '触发器';


--
-- Name: COLUMN task_node.trigger_args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.trigger_args IS '触发器参数';


--
-- Name: COLUMN task_node.func; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.func IS '代码块';


--
-- Name: COLUMN task_node.args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.args IS '位置参数';


--
-- Name: COLUMN task_node.kwargs; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.kwargs IS '关键字参数';


--
-- Name: COLUMN task_node."coalesce"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node."coalesce" IS '是否合并运行';


--
-- Name: COLUMN task_node.max_instances; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.max_instances IS '最大实例数';


--
-- Name: COLUMN task_node.start_date; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.start_date IS '开始时间';


--
-- Name: COLUMN task_node.end_date; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.end_date IS '结束时间';


--
-- Name: COLUMN task_node.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.id IS '主键ID';


--
-- Name: COLUMN task_node.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_node.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN task_node.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.description IS '备注/描述';


--
-- Name: COLUMN task_node.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.created_time IS '创建时间';


--
-- Name: COLUMN task_node.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.updated_time IS '更新时间';


--
-- Name: COLUMN task_node.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.created_id IS '创建人ID';


--
-- Name: COLUMN task_node.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_node.updated_id IS '更新人ID';


--
-- Name: task_node_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.task_node_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_node_id_seq OWNER TO tao;

--
-- Name: task_node_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.task_node_id_seq OWNED BY public.task_node.id;


--
-- Name: task_workflow; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.task_workflow (
    name character varying(128) NOT NULL,
    code character varying(64) NOT NULL,
    status character varying(32) NOT NULL,
    nodes json NOT NULL,
    edges json NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.task_workflow OWNER TO tao;

--
-- Name: TABLE task_workflow; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.task_workflow IS '工作流表';


--
-- Name: COLUMN task_workflow.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.name IS '流程名称';


--
-- Name: COLUMN task_workflow.code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.code IS '流程编码';


--
-- Name: COLUMN task_workflow.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.status IS '流程状态';


--
-- Name: COLUMN task_workflow.nodes; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.nodes IS '节点数据(JSON格式)';


--
-- Name: COLUMN task_workflow.edges; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.edges IS '连线数据(JSON格式)';


--
-- Name: COLUMN task_workflow.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.id IS '主键ID';


--
-- Name: COLUMN task_workflow.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_workflow.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.description IS '备注/描述';


--
-- Name: COLUMN task_workflow.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.created_time IS '创建时间';


--
-- Name: COLUMN task_workflow.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.updated_time IS '更新时间';


--
-- Name: COLUMN task_workflow.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.created_id IS '创建人ID';


--
-- Name: COLUMN task_workflow.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.task_workflow.updated_id IS '更新人ID';


--
-- Name: task_workflow_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.task_workflow_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_workflow_id_seq OWNER TO tao;

--
-- Name: task_workflow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.task_workflow_id_seq OWNED BY public.task_workflow.id;


--
-- Name: ai_chat_message id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.ai_chat_message ALTER COLUMN id SET DEFAULT nextval('public.ai_chat_message_id_seq'::regclass);


--
-- Name: ai_chat_session id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.ai_chat_session ALTER COLUMN id SET DEFAULT nextval('public.ai_chat_session_id_seq'::regclass);


--
-- Name: app_myapp id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_myapp ALTER COLUMN id SET DEFAULT nextval('public.app_myapp_id_seq'::regclass);


--
-- Name: gen_demo id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_demo ALTER COLUMN id SET DEFAULT nextval('public.gen_demo_id_seq'::regclass);


--
-- Name: gen_table id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table ALTER COLUMN id SET DEFAULT nextval('public.gen_table_id_seq'::regclass);


--
-- Name: gen_table_column id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column ALTER COLUMN id SET DEFAULT nextval('public.gen_table_column_id_seq'::regclass);


--
-- Name: sys_dept id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dept ALTER COLUMN id SET DEFAULT nextval('public.sys_dept_id_seq'::regclass);


--
-- Name: sys_dict_data id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_data ALTER COLUMN id SET DEFAULT nextval('public.sys_dict_data_id_seq'::regclass);


--
-- Name: sys_dict_type id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_type ALTER COLUMN id SET DEFAULT nextval('public.sys_dict_type_id_seq'::regclass);


--
-- Name: sys_log id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_log ALTER COLUMN id SET DEFAULT nextval('public.sys_log_id_seq'::regclass);


--
-- Name: sys_menu id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_menu ALTER COLUMN id SET DEFAULT nextval('public.sys_menu_id_seq'::regclass);


--
-- Name: sys_notice id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_notice ALTER COLUMN id SET DEFAULT nextval('public.sys_notice_id_seq'::regclass);


--
-- Name: sys_param id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_param ALTER COLUMN id SET DEFAULT nextval('public.sys_param_id_seq'::regclass);


--
-- Name: sys_position id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_position ALTER COLUMN id SET DEFAULT nextval('public.sys_position_id_seq'::regclass);


--
-- Name: sys_role id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role ALTER COLUMN id SET DEFAULT nextval('public.sys_role_id_seq'::regclass);


--
-- Name: sys_user id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user ALTER COLUMN id SET DEFAULT nextval('public.sys_user_id_seq'::regclass);


--
-- Name: task_job id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_job ALTER COLUMN id SET DEFAULT nextval('public.task_job_id_seq'::regclass);


--
-- Name: task_node id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_node ALTER COLUMN id SET DEFAULT nextval('public.task_node_id_seq'::regclass);


--
-- Name: task_workflow id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_workflow ALTER COLUMN id SET DEFAULT nextval('public.task_workflow_id_seq'::regclass);


--
-- Data for Name: ai_chat_message; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.ai_chat_message (session_id, type, content, "timestamp", files, id, uuid, status, description, created_time, updated_time) FROM stdin;
\.


--
-- Data for Name: ai_chat_session; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.ai_chat_session (title, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: app_myapp; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.app_myapp (name, access_url, icon_url, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: apscheduler_jobs; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.apscheduler_jobs (id, next_run_time, job_state) FROM stdin;
\.


--
-- Data for Name: gen_demo; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.gen_demo (name, a, b, c, d, e, f, g, h, i, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: gen_table; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.gen_table (table_name, table_comment, class_name, package_name, module_name, business_name, function_name, sub_table_name, sub_table_fk_name, parent_menu_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: gen_table_column; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.gen_table_column (column_name, column_comment, column_type, column_length, column_default, is_pk, is_increment, is_nullable, is_unique, python_type, python_field, is_insert, is_edit, is_list, is_query, query_type, html_type, dict_type, sort, table_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_dept; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_dept (name, "order", code, leader, phone, email, parent_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
集团总公司	1	GROUP	部门负责人	1582112620	deptadmin@example.com	\N	1	0d48a02f-a479-42a2-9184-fcb60de31cf4	0	集团总公司	2026-02-23 06:41:21.185814	2026-02-23 06:41:21.185816
\.


--
-- Data for Name: sys_dict_data; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_dict_data (dict_sort, dict_label, dict_value, css_class, list_class, is_default, dict_type, dict_type_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
1	男	0	blue	\N	t	sys_user_sex	1	1	ae2e4474-b930-46b9-99f1-23a58ebcd8ca	0	性别男	2026-02-23 06:41:21.194454	2026-02-23 06:41:21.194455
2	女	1	pink	\N	f	sys_user_sex	1	2	ccde0db1-9d74-4021-82cb-ca5c327a1677	0	性别女	2026-02-23 06:41:21.194458	2026-02-23 06:41:21.194459
3	未知	2	red	\N	f	sys_user_sex	1	3	33ad5961-668f-46ea-a0b2-892d8eb0977e	0	性别未知	2026-02-23 06:41:21.194462	2026-02-23 06:41:21.194462
1	是	1		primary	t	sys_yes_no	2	4	28358675-2070-4195-9f1c-6cd40102fea1	0	是	2026-02-23 06:41:21.194465	2026-02-23 06:41:21.194465
2	否	0		danger	f	sys_yes_no	2	5	648a9740-696b-4839-89c2-d0cc85a2d1d2	0	否	2026-02-23 06:41:21.194468	2026-02-23 06:41:21.194469
1	启用	1		primary	f	sys_common_status	3	6	148d4531-b794-485d-908e-babdd6a9cc7b	0	启用状态	2026-02-23 06:41:21.194471	2026-02-23 06:41:21.194472
2	停用	0		danger	f	sys_common_status	3	7	31deab15-f8e6-48d2-9d82-537ea032e109	0	停用状态	2026-02-23 06:41:21.194474	2026-02-23 06:41:21.194475
1	通知	1	blue	warning	t	sys_notice_type	4	8	320a2c92-782d-4881-833f-52b3db6d21ce	0	通知	2026-02-23 06:41:21.194478	2026-02-23 06:41:21.194478
2	公告	2	orange	success	f	sys_notice_type	4	9	91d174c5-070a-4760-908a-563836a7a1aa	0	公告	2026-02-23 06:41:21.194481	2026-02-23 06:41:21.194481
99	其他	0		info	f	sys_oper_type	5	10	d32c5ee2-428c-4bc5-9821-c7170540d3c3	0	其他操作	2026-02-23 06:41:21.194484	2026-02-23 06:41:21.194484
1	新增	1		info	f	sys_oper_type	5	11	d1b3fdd0-2d30-4dcf-ae91-9c2dcebaaadd	0	新增操作	2026-02-23 06:41:21.194487	2026-02-23 06:41:21.194487
2	修改	2		info	f	sys_oper_type	5	12	114145b9-d557-4907-bf72-0b1540eb18f0	0	修改操作	2026-02-23 06:41:21.19449	2026-02-23 06:41:21.19449
3	删除	3		danger	f	sys_oper_type	5	13	f84502e2-c63a-4f1f-89b9-1e518e84c44d	0	删除操作	2026-02-23 06:41:21.194493	2026-02-23 06:41:21.194493
4	分配权限	4		primary	f	sys_oper_type	5	14	2e5edbec-ef03-4781-9d86-9db517147564	0	授权操作	2026-02-23 06:41:21.194496	2026-02-23 06:41:21.194496
5	导出	5		warning	f	sys_oper_type	5	15	b2d0e4d7-0b26-409b-9051-491dbfc248fe	0	导出操作	2026-02-23 06:41:21.194499	2026-02-23 06:41:21.194499
6	导入	6		warning	f	sys_oper_type	5	16	83c65505-1821-48bd-827f-ac13804a6def	0	导入操作	2026-02-23 06:41:21.194502	2026-02-23 06:41:21.194502
7	强退	7		danger	f	sys_oper_type	5	17	5415c09e-9a7f-4ca3-9ef6-90ca890994aa	0	强退操作	2026-02-23 06:41:21.194505	2026-02-23 06:41:21.194505
8	生成代码	8		warning	f	sys_oper_type	5	18	b7f08bdb-213e-4941-b024-4613aafe03e8	0	生成操作	2026-02-23 06:41:21.194508	2026-02-23 06:41:21.194508
9	清空数据	9		danger	f	sys_oper_type	5	19	8857d02d-84d8-4400-a23b-27188d06eebe	0	清空操作	2026-02-23 06:41:21.194511	2026-02-23 06:41:21.194511
1	默认(Memory)	default		\N	t	sys_job_store	6	20	7ac87b85-7671-4f69-89b2-558a6a1827d2	0	默认分组	2026-02-23 06:41:21.194514	2026-02-23 06:41:21.194514
2	数据库(Sqlalchemy)	sqlalchemy		\N	f	sys_job_store	6	21	962791aa-f749-4c62-a5a4-d6c5a743dd75	0	数据库分组	2026-02-23 06:41:21.194517	2026-02-23 06:41:21.194517
3	数据库(Redis)	redis		\N	f	sys_job_store	6	22	50b89677-0b69-4ab9-aa54-738402e50d3d	0	reids分组	2026-02-23 06:41:21.19452	2026-02-23 06:41:21.19452
1	线程池	default		\N	f	sys_job_executor	7	23	4dac62b0-cbd8-4b84-8cd1-da6e9022db86	0	线程池	2026-02-23 06:41:21.194523	2026-02-23 06:41:21.194523
2	进程池	processpool		\N	f	sys_job_executor	7	24	640ba58c-926a-4428-9181-eef1a296b061	0	进程池	2026-02-23 06:41:21.194526	2026-02-23 06:41:21.194526
1	演示函数	scheduler_test.job		\N	t	sys_job_function	8	25	ed29e0f4-c5e8-433d-ad19-3e6ea3b983ae	0	演示函数	2026-02-23 06:41:21.194529	2026-02-23 06:41:21.194529
1	指定日期(date)	date		\N	t	sys_job_trigger	9	26	4d89a37b-52b4-4436-9649-7ef21a2f520d	0	指定日期任务触发器	2026-02-23 06:41:21.194532	2026-02-23 06:41:21.194533
2	间隔触发器(interval)	interval		\N	f	sys_job_trigger	9	27	25c0a69e-a84d-4f73-a7dd-c03745164cbf	0	间隔触发器任务触发器	2026-02-23 06:41:21.194535	2026-02-23 06:41:21.194536
3	cron表达式	cron		\N	f	sys_job_trigger	9	28	7aab6858-fed8-40bf-bbfe-810118cac5d8	0	间隔触发器任务触发器	2026-02-23 06:41:21.194538	2026-02-23 06:41:21.194539
1	默认(default)	default		\N	t	sys_list_class	10	29	9255f2db-d624-47cf-ba5a-9f29f42e3416	0	默认表格回显样式	2026-02-23 06:41:21.194541	2026-02-23 06:41:21.194542
2	主要(primary)	primary		\N	f	sys_list_class	10	30	ebb427b1-7234-430e-a092-c26aa8e8bb82	0	主要表格回显样式	2026-02-23 06:41:21.194544	2026-02-23 06:41:21.194545
3	成功(success)	success		\N	f	sys_list_class	10	31	919d9a6d-b853-4f51-afa8-6ca61ecf505c	0	成功表格回显样式	2026-02-23 06:41:21.194547	2026-02-23 06:41:21.194548
4	信息(info)	info		\N	f	sys_list_class	10	32	15c10cff-733c-47fa-9f5d-de2f5b9f1225	0	信息表格回显样式	2026-02-23 06:41:21.19455	2026-02-23 06:41:21.194551
5	警告(warning)	warning		\N	f	sys_list_class	10	33	0ec5c7c0-f7eb-4f34-badc-8d234f35ea60	0	警告表格回显样式	2026-02-23 06:41:21.194554	2026-02-23 06:41:21.194554
6	危险(danger)	danger		\N	f	sys_list_class	10	34	3265d095-ea57-451b-8b8b-56132ace3097	0	危险表格回显样式	2026-02-23 06:41:21.194557	2026-02-23 06:41:21.194557
\.


--
-- Data for Name: sys_dict_type; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_dict_type (dict_name, dict_type, id, uuid, status, description, created_time, updated_time) FROM stdin;
用户性别	sys_user_sex	1	748a68f0-7e38-4ef4-a78c-c220696b1c2a	0	用户性别列表	2026-02-23 06:41:21.190098	2026-02-23 06:41:21.1901
系统是否	sys_yes_no	2	542ab2d7-b8dd-4661-803d-af142730b412	0	系统是否列表	2026-02-23 06:41:21.190104	2026-02-23 06:41:21.190104
系统状态	sys_common_status	3	9e24a697-22ee-4aa4-a440-af515be316fe	0	系统状态	2026-02-23 06:41:21.190107	2026-02-23 06:41:21.190108
通知类型	sys_notice_type	4	11c8616c-c4b2-455d-9753-a6087557d3fc	0	通知类型列表	2026-02-23 06:41:21.190128	2026-02-23 06:41:21.190128
操作类型	sys_oper_type	5	26eb0b49-6928-4dc8-839e-d6ead9420033	0	操作类型列表	2026-02-23 06:41:21.190139	2026-02-23 06:41:21.190139
任务存储器	sys_job_store	6	d8e24792-3d76-44e3-9e34-5b01fc394ae1	0	任务分组列表	2026-02-23 06:41:21.190142	2026-02-23 06:41:21.190142
任务执行器	sys_job_executor	7	f03ceb19-3cb5-43af-b920-fcae9745c16e	0	任务执行器列表	2026-02-23 06:41:21.190145	2026-02-23 06:41:21.190146
任务函数	sys_job_function	8	52e613c5-6221-4fa5-a8c3-3e73f9e25126	0	任务函数列表	2026-02-23 06:41:21.190149	2026-02-23 06:41:21.190149
任务触发器	sys_job_trigger	9	4561eabf-04ed-4bc2-bcad-87816467da0f	0	任务触发器列表	2026-02-23 06:41:21.190152	2026-02-23 06:41:21.190152
表格回显样式	sys_list_class	10	5da610f7-b0fc-4687-8818-59c2d5438a46	0	表格回显样式列表	2026-02-23 06:41:21.190155	2026-02-23 06:41:21.190156
\.


--
-- Data for Name: sys_log; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_log (type, request_path, request_method, request_payload, request_ip, login_location, request_os, request_browser, response_code, response_json, process_time, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_menu; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_menu (name, type, "order", permission, icon, route_name, route_path, component_path, redirect, hidden, keep_alive, always_show, title, params, affix, parent_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
仪表盘	1	1		client	Dashboard	/dashboard	\N	/dashboard/workplace	f	t	t	仪表盘	null	f	\N	1	8b0bfbcb-2902-45f6-aa27-4b90ac993e2f	0	初始化数据	2026-02-23 06:41:21.165304	2026-02-23 06:41:21.16531
系统管理	1	2	\N	system	System	/system	\N	/system/menu	f	t	f	系统管理	null	f	\N	2	899c36e3-2596-4b12-b409-5b601cf32816	0	初始化数据	2026-02-23 06:41:21.165315	2026-02-23 06:41:21.165315
监控管理	1	3	\N	monitor	Monitor	/monitor	\N	/monitor/online	f	t	f	监控管理	null	f	\N	3	1a987da0-c978-4252-a510-bba4e61f27d5	0	初始化数据	2026-02-23 06:41:21.165318	2026-02-23 06:41:21.165319
接口管理	1	4	\N	document	Common	/common	\N	/common/docs	f	t	f	接口管理	null	f	\N	4	20468f06-88d0-4d98-8f66-ad1c6172d985	0	初始化数据	2026-02-23 06:41:21.165322	2026-02-23 06:41:21.165322
代码管理	1	5	\N	code	Generator	/generator	\N	/generator/gencode	f	t	f	代码管理	null	f	\N	5	165f272d-c707-4798-9a8c-de3c28ceca38	0	代码管理	2026-02-23 06:41:21.165325	2026-02-23 06:41:21.165325
应用管理	1	6	\N	el-icon-ShoppingBag	Application	/application	\N	/application/myapp	f	t	f	应用管理	null	f	\N	6	35727681-24ec-4fdd-9a26-53b45cb02d96	0	初始化数据	2026-02-23 06:41:21.165328	2026-02-23 06:41:21.165328
AI管理	1	7	\N	el-icon-ChatLineSquare	AI	/ai	\N	/ai/chat	f	t	f	AI管理	null	f	\N	7	7fd1aff6-cd92-493e-8c30-1224576b3085	0	AI管理	2026-02-23 06:41:21.165331	2026-02-23 06:41:21.165331
任务管理	1	8	\N	el-icon-SetUp	Task	/task	\N	/task/job	f	t	f	任务管理	null	f	\N	8	937380d7-bb38-49a1-bc5e-76733aff9cae	0	任务管理	2026-02-23 06:41:21.165334	2026-02-23 06:41:21.165335
案例管理	1	9	\N	menu	Example	/example	\N	/example/demo	f	t	f	案例管理	null	f	\N	9	213d1531-f70d-4fb0-b88b-4572891b33d6	0	案例管理	2026-02-23 06:41:21.165337	2026-02-23 06:41:21.165338
工作台	2	1	dashboard:workplace:query	el-icon-PieChart	Workplace	/dashboard/workplace	dashboard/workplace	\N	f	t	f	工作台	null	f	1	10	1f123ae5-573f-448e-bed8-9f38f3685ac1	0	初始化数据	2026-02-23 06:41:21.168756	2026-02-23 06:41:21.168758
菜单管理	2	1	module_system:menu:query	menu	Menu	/system/menu	module_system/menu/index	\N	f	t	f	菜单管理	null	f	2	11	6fa49e7e-764b-46bd-bc4e-45886f49e0cd	0	初始化数据	2026-02-23 06:41:21.168761	2026-02-23 06:41:21.168762
部门管理	2	2	module_system:dept:query	tree	Dept	/system/dept	module_system/dept/index	\N	f	t	f	部门管理	null	f	2	12	5eb9be79-b802-4b31-8998-5c9fa0d7231f	0	初始化数据	2026-02-23 06:41:21.168765	2026-02-23 06:41:21.168765
岗位管理	2	3	module_system:position:query	el-icon-Coordinate	Position	/system/position	module_system/position/index	\N	f	t	f	岗位管理	null	f	2	13	2be648d0-0b31-4262-859b-f15cff2a905a	0	初始化数据	2026-02-23 06:41:21.168768	2026-02-23 06:41:21.168768
角色管理	2	4	module_system:role:query	role	Role	/system/role	module_system/role/index	\N	f	t	f	角色管理	null	f	2	14	171f132f-7802-4d83-b562-68ccd527b7b4	0	初始化数据	2026-02-23 06:41:21.168771	2026-02-23 06:41:21.168771
用户管理	2	5	module_system:user:query	el-icon-User	User	/system/user	module_system/user/index	\N	f	t	f	用户管理	null	f	2	15	1cb66ff5-a3ad-496c-9044-23aeef9c073b	0	初始化数据	2026-02-23 06:41:21.168774	2026-02-23 06:41:21.168775
日志管理	2	6	module_system:log:query	el-icon-Aim	Log	/system/log	module_system/log/index	\N	f	t	f	日志管理	null	f	2	16	93c592c8-2897-4bcf-bd16-89dc3b36de0e	0	初始化数据	2026-02-23 06:41:21.168777	2026-02-23 06:41:21.168778
公告管理	2	7	module_system:notice:query	bell	Notice	/system/notice	module_system/notice/index	\N	f	t	f	公告管理	null	f	2	17	04c03041-af2f-42a6-b54e-04508077f83e	0	初始化数据	2026-02-23 06:41:21.168781	2026-02-23 06:41:21.168782
参数管理	2	8	module_system:param:query	setting	Params	/system/param	module_system/param/index	\N	f	t	f	参数管理	null	f	2	18	df748b11-7bf7-494b-98bc-d14cdf5982bb	0	初始化数据	2026-02-23 06:41:21.168784	2026-02-23 06:41:21.168785
字典管理	2	9	module_system:dict_type:query	dict	Dict	/system/dict	module_system/dict/index	\N	f	t	f	字典管理	null	f	2	19	e59c0c18-d70e-45a4-b536-94787f58e57f	0	初始化数据	2026-02-23 06:41:21.168787	2026-02-23 06:41:21.168788
在线用户	2	1	module_monitor:online:query	el-icon-Headset	MonitorOnline	/monitor/online	module_monitor/online/index	\N	f	t	f	在线用户	null	f	3	20	6dd1fd9f-f80e-4cf2-86f5-f37d8d4fb104	0	初始化数据	2026-02-23 06:41:21.16879	2026-02-23 06:41:21.168791
服务器监控	2	2	module_monitor:server:query	el-icon-Odometer	MonitorServer	/monitor/server	module_monitor/server/index	\N	f	t	f	服务器监控	null	f	3	21	b7b199bf-fd67-435c-9141-541fdd529d2c	0	初始化数据	2026-02-23 06:41:21.168793	2026-02-23 06:41:21.168794
缓存监控	2	3	module_monitor:cache:query	el-icon-Stopwatch	MonitorCache	/monitor/cache	module_monitor/cache/index	\N	f	t	f	缓存监控	null	f	3	22	bac2cdd6-8ac5-438b-b81e-b9dc91b970b7	0	初始化数据	2026-02-23 06:41:21.168796	2026-02-23 06:41:21.168796
文件管理	2	4	module_monitor:resource:query	el-icon-Files	Resource	/monitor/resource	module_monitor/resource/index	\N	f	t	f	文件管理	null	f	3	23	81e2f28b-6c70-4a8c-a67f-c7f14769470d	0	初始化数据	2026-02-23 06:41:21.168799	2026-02-23 06:41:21.168799
Swagger文档	4	1	module_common:docs:query	api	Docs	/common/docs	module_common/docs/index	\N	f	t	f	Swagger文档	null	f	4	24	6f975231-c1dd-43ac-9b5a-29b170cb67fa	0	初始化数据	2026-02-23 06:41:21.168802	2026-02-23 06:41:21.168802
Redoc文档	4	2	module_common:redoc:query	el-icon-Document	Redoc	/common/redoc	module_common/redoc/index	\N	f	t	f	Redoc文档	null	f	4	25	e977ff89-a082-4676-85eb-6cc4ad852ba8	0	初始化数据	2026-02-23 06:41:21.168805	2026-02-23 06:41:21.168805
LangJin文档	4	3	module_common:ljdoc:query	el-icon-Document	Ljdoc	/common/ljdoc	module_common/ljdoc/index	\N	f	t	f	LangJin文档	null	f	4	26	d524f89b-688c-4721-b2a5-15a6c85c93b8	0	初始化数据	2026-02-23 06:41:21.168808	2026-02-23 06:41:21.168808
代码生成	2	1	module_generator:gencode:query	code	GenCode	/generator/gencode	module_generator/gencode/index	\N	f	t	f	代码生成	null	f	5	27	569bbc1b-a819-4cd0-8632-53b67d92eb11	0	代码生成	2026-02-23 06:41:21.168811	2026-02-23 06:41:21.168812
我的应用	2	1	module_application:myapp:query	el-icon-ShoppingCartFull	MYAPP	/application/myapp	module_application/myapp/index	\N	f	t	f	我的应用	null	f	6	28	34851479-acfd-4129-9ee2-3ba4112f9321	0	初始化数据	2026-02-23 06:41:21.168814	2026-02-23 06:41:21.168815
会话标题	2	1	module_ai:chat_session:query	el-icon-ChatLineRound	ChatSession	/ai/chat_session	module_ai/chat_session/index	\N	f	t	f	会话标题	null	f	7	29	d1afdd54-0672-470c-a0ed-b77eb1c9a51b	0	会话标题	2026-02-23 06:41:21.168817	2026-02-23 06:41:21.168818
会话内容	2	2	module_ai:chat_message:query	el-icon-ChatSquare	ChatMessage	/ai/chat_message	module_ai/chat_message/index	\N	f	t	f	会话内容	null	f	7	30	e15ed9b6-acc0-43aa-bb65-51250302fc72	0	会话内容	2026-02-23 06:41:21.16882	2026-02-23 06:41:21.168821
AI智能助手	2	3	module_ai:chat:ws	el-icon-ChatDotRound	Chat	/application/ai	module_ai/chat/index	\N	f	t	f	AI智能助手	null	f	7	31	f21af8cf-ea67-4e3e-90d3-8425e2b00de5	0	AI智能助手	2026-02-23 06:41:21.168823	2026-02-23 06:41:21.168824
调度器监控	2	1	module_task:job:query	el-icon-DataLine	Job	/task/job	module_task/job/index	\N	f	t	f	调度器监控	null	f	8	32	bd0ff214-a9d0-45f8-a220-2ced1057fa8f	0	调度器监控	2026-02-23 06:41:21.168827	2026-02-23 06:41:21.168828
节点管理	2	2	module_task:node:query	el-icon-Postcard	Node	/task/node	module_task/node/index	\N	f	t	f	节点管理	null	f	8	33	d96e7a7e-a029-423f-9f04-cff2d211a170	0	节点管理	2026-02-23 06:41:21.168831	2026-02-23 06:41:21.168832
流程编排	2	3	module_task:workflow:query	el-icon-Share	Workflow	/task/workflow	module_task/workflow/index	\N	f	t	f	流程编排	null	f	8	34	7c9c80d9-0a09-4954-beed-fb95bb9bba61	0	流程编排	2026-02-23 06:41:21.168836	2026-02-23 06:41:21.168836
示例管理	2	1	module_example:demo:query	menu	Demo	/example/demo	module_example/demo/index	\N	f	t	f	示例管理	null	f	9	35	2367e72e-fec8-4fe5-aad4-5e72ead23207	0	示例管理	2026-02-23 06:41:21.16884	2026-02-23 06:41:21.16884
创建菜单	3	1	module_system:menu:create	\N	\N	\N	\N	\N	f	t	f	创建菜单	null	f	11	36	cd2b49d4-3565-4430-9956-b1988d2bc335	0	初始化数据	2026-02-23 06:41:21.173505	2026-02-23 06:41:21.173507
修改菜单	3	2	module_system:menu:update	\N	\N	\N	\N	\N	f	t	f	修改菜单	null	f	11	37	73911eeb-df86-4f82-af41-a616cdc1b181	0	初始化数据	2026-02-23 06:41:21.173512	2026-02-23 06:41:21.173512
删除菜单	3	3	module_system:menu:delete	\N	\N	\N	\N	\N	f	t	f	删除菜单	null	f	11	38	50bef276-f801-40ae-8cc6-39f23dfe903e	0	初始化数据	2026-02-23 06:41:21.173515	2026-02-23 06:41:21.173516
批量修改菜单状态	3	4	module_system:menu:patch	\N	\N	\N	\N	\N	f	t	f	批量修改菜单状态	null	f	11	39	e6988f19-8da3-4fd8-836d-06372293beb2	0	初始化数据	2026-02-23 06:41:21.173519	2026-02-23 06:41:21.173519
详情菜单	3	5	module_system:menu:detail	\N	\N	\N	\N	\N	f	t	f	详情菜单	null	f	11	40	646219c5-ad2a-41d6-a79a-e66c04282979	0	初始化数据	2026-02-23 06:41:21.173522	2026-02-23 06:41:21.173523
查询菜单	3	6	module_system:menu:query	\N	\N	\N	\N	\N	f	t	f	查询菜单	null	f	11	41	314c094f-bda2-4254-a859-d37727276112	0	初始化数据	2026-02-23 06:41:21.173526	2026-02-23 06:41:21.173526
创建部门	3	1	module_system:dept:create	\N	\N	\N	\N	\N	f	t	f	创建部门	null	f	12	42	6b2660f0-2dfe-498c-8a87-eddaf5459e1c	0	初始化数据	2026-02-23 06:41:21.173529	2026-02-23 06:41:21.17353
修改部门	3	2	module_system:dept:update	\N	\N	\N	\N	\N	f	t	f	修改部门	null	f	12	43	5fc013ff-afdb-4814-aa37-ca3f3d393b39	0	初始化数据	2026-02-23 06:41:21.173532	2026-02-23 06:41:21.173533
删除部门	3	3	module_system:dept:delete	\N	\N	\N	\N	\N	f	t	f	删除部门	null	f	12	44	ee5177eb-1d36-43c1-a97b-5641d718203c	0	初始化数据	2026-02-23 06:41:21.173536	2026-02-23 06:41:21.173536
批量修改部门状态	3	4	module_system:dept:patch	\N	\N	\N	\N	\N	f	t	f	批量修改部门状态	null	f	12	45	f4c8f88f-eabd-4193-a720-16a56e56037b	0	初始化数据	2026-02-23 06:41:21.173539	2026-02-23 06:41:21.173539
详情部门	3	5	module_system:dept:detail	\N	\N	\N	\N	\N	f	t	f	详情部门	null	f	12	46	5b78441e-652f-42c2-8ef8-f9870f30ba3b	0	初始化数据	2026-02-23 06:41:21.173542	2026-02-23 06:41:21.173543
查询部门	3	6	module_system:dept:query	\N	\N	\N	\N	\N	f	t	f	查询部门	null	f	12	47	0493c602-fbe3-4d42-b668-3c5678e85b3c	0	初始化数据	2026-02-23 06:41:21.173547	2026-02-23 06:41:21.173547
创建岗位	3	1	module_system:position:create	\N	\N	\N	\N	\N	f	t	f	创建岗位	null	f	13	48	87ac2883-f536-48a2-a2c7-bce9eddf3163	0	初始化数据	2026-02-23 06:41:21.17355	2026-02-23 06:41:21.17355
修改岗位	3	2	module_system:position:update	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	13	49	4b66be05-e453-40d9-a4e4-06f66044809f	0	初始化数据	2026-02-23 06:41:21.173553	2026-02-23 06:41:21.173554
删除岗位	3	3	module_system:position:delete	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	13	50	4d602af8-49b6-4d6c-8710-a9a14942da3e	0	初始化数据	2026-02-23 06:41:21.173556	2026-02-23 06:41:21.173557
批量修改岗位状态	3	4	module_system:position:patch	\N	\N	\N	\N	\N	f	t	f	批量修改岗位状态	null	f	13	51	42b68bae-b723-442f-84d1-95965ffaf44e	0	初始化数据	2026-02-23 06:41:21.17356	2026-02-23 06:41:21.17356
岗位导出	3	5	module_system:position:export	\N	\N	\N	\N	\N	f	t	f	岗位导出	null	f	13	52	8614414f-8867-41bf-a8c9-e55331d06a6f	0	初始化数据	2026-02-23 06:41:21.173563	2026-02-23 06:41:21.173563
详情岗位	3	6	module_system:position:detail	\N	\N	\N	\N	\N	f	t	f	详情岗位	null	f	13	53	0ff1a35d-a153-442b-a111-563935233647	0	初始化数据	2026-02-23 06:41:21.173566	2026-02-23 06:41:21.173566
查询岗位	3	7	module_system:position:query	\N	\N	\N	\N	\N	f	t	f	查询岗位	null	f	13	54	5ea3cd79-a159-4821-b4b3-8aa986f1e1bf	0	初始化数据	2026-02-23 06:41:21.173569	2026-02-23 06:41:21.173569
创建角色	3	1	module_system:role:create	\N	\N	\N	\N	\N	f	t	f	创建角色	null	f	14	55	57c451c5-b269-44bc-a110-f1f1a8c9ae94	0	初始化数据	2026-02-23 06:41:21.173572	2026-02-23 06:41:21.173572
修改角色	3	2	module_system:role:update	\N	\N	\N	\N	\N	f	t	f	修改角色	null	f	14	56	e90161b1-c2ac-4bbb-8e97-46e5ebbf4074	0	初始化数据	2026-02-23 06:41:21.173575	2026-02-23 06:41:21.173575
删除角色	3	3	module_system:role:delete	\N	\N	\N	\N	\N	f	t	f	删除角色	null	f	14	57	825396fd-f8ce-4a05-b333-0ce3dea0efe8	0	初始化数据	2026-02-23 06:41:21.173578	2026-02-23 06:41:21.173578
批量修改角色状态	3	4	module_system:role:patch	\N	\N	\N	\N	\N	f	t	f	批量修改角色状态	null	f	14	58	45158ae0-d377-4a07-b56e-20b8e66878fb	0	初始化数据	2026-02-23 06:41:21.173581	2026-02-23 06:41:21.173581
角色导出	3	5	module_system:role:export	\N	\N	\N	\N	\N	f	t	f	角色导出	null	f	14	59	f06fd447-e643-411a-81df-09e37a5131c2	0	初始化数据	2026-02-23 06:41:21.173584	2026-02-23 06:41:21.173585
详情角色	3	6	module_system:role:detail	\N	\N	\N	\N	\N	f	t	f	详情角色	null	f	14	60	4ae7180a-9d37-47e3-bd46-a17b582467e5	0	初始化数据	2026-02-23 06:41:21.173587	2026-02-23 06:41:21.173588
查询角色	3	7	module_system:role:query	\N	\N	\N	\N	\N	f	t	f	查询角色	null	f	14	61	0c2c2d09-2516-4a9c-bbdb-735a35040a77	0	初始化数据	2026-02-23 06:41:21.17359	2026-02-23 06:41:21.173591
分配权限	3	8	module_system:role:permission	\N	\N	\N	\N	\N	f	t	f	分配权限	null	f	14	62	dc23b37f-fc5d-40d6-b7a2-2b3481e3b401	0	初始化数据	2026-02-23 06:41:21.173593	2026-02-23 06:41:21.173594
创建用户	3	1	module_system:user:create	\N	\N	\N	\N	\N	f	t	f	创建用户	null	f	15	63	48fdfc48-80ff-4e1f-a671-50077aba142a	0	初始化数据	2026-02-23 06:41:21.173596	2026-02-23 06:41:21.173597
修改用户	3	2	module_system:user:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	15	64	3e40b761-0bda-4f5f-a9e6-958b2a1f187c	0	初始化数据	2026-02-23 06:41:21.1736	2026-02-23 06:41:21.1736
删除用户	3	3	module_system:user:delete	\N	\N	\N	\N	\N	f	t	f	删除用户	null	f	15	65	2163a39a-ca30-4fcd-a7a1-92ebc62eb051	0	初始化数据	2026-02-23 06:41:21.173603	2026-02-23 06:41:21.173603
批量修改用户状态	3	4	module_system:user:patch	\N	\N	\N	\N	\N	f	t	f	批量修改用户状态	null	f	15	66	de042b7c-995c-4f23-a2de-41e77b10dc23	0	初始化数据	2026-02-23 06:41:21.173606	2026-02-23 06:41:21.173606
导出用户	3	5	module_system:user:export	\N	\N	\N	\N	\N	f	t	f	导出用户	null	f	15	67	fe311438-fd4d-4adf-9056-3726073a2bbf	0	初始化数据	2026-02-23 06:41:21.173609	2026-02-23 06:41:21.173609
导入用户	3	6	module_system:user:import	\N	\N	\N	\N	\N	f	t	f	导入用户	null	f	15	68	119e4389-d41e-4cc1-9a83-bb95e9c143de	0	初始化数据	2026-02-23 06:41:21.173612	2026-02-23 06:41:21.173612
下载用户导入模板	3	7	module_system:user:download	\N	\N	\N	\N	\N	f	t	f	下载用户导入模板	null	f	15	69	c0344cf3-db7d-4a44-941b-b238a9a281b4	0	初始化数据	2026-02-23 06:41:21.173615	2026-02-23 06:41:21.173615
详情用户	3	8	module_system:user:detail	\N	\N	\N	\N	\N	f	t	f	详情用户	null	f	15	70	e6211e68-4432-42e8-9cfe-4051b456a8f2	0	初始化数据	2026-02-23 06:41:21.173618	2026-02-23 06:41:21.173618
查询用户	3	9	module_system:user:query	\N	\N	\N	\N	\N	f	t	f	查询用户	null	f	15	71	3bf90a8a-05be-4c91-a30b-2231b074477f	0	初始化数据	2026-02-23 06:41:21.173621	2026-02-23 06:41:21.173621
日志删除	3	1	module_system:log:delete	\N	\N	\N	\N	\N	f	t	f	日志删除	null	f	16	72	7f69f46d-c302-4b3d-be5f-e5fd71bdb3ab	0	初始化数据	2026-02-23 06:41:21.173624	2026-02-23 06:41:21.173624
日志导出	3	2	module_system:log:export	\N	\N	\N	\N	\N	f	t	f	日志导出	null	f	16	73	63aafebe-a4a2-4558-bd76-0e977e7ef820	0	初始化数据	2026-02-23 06:41:21.173627	2026-02-23 06:41:21.173628
日志详情	3	3	module_system:log:detail	\N	\N	\N	\N	\N	f	t	f	日志详情	null	f	16	74	aa50293f-1dfe-4ec2-b733-99cbd352866d	0	初始化数据	2026-02-23 06:41:21.17363	2026-02-23 06:41:21.173631
查询日志	3	4	module_system:log:query	\N	\N	\N	\N	\N	f	t	f	查询日志	null	f	16	75	5a7b0c16-a52d-47cc-8ca0-3887bab398cf	0	初始化数据	2026-02-23 06:41:21.173633	2026-02-23 06:41:21.173634
公告创建	3	1	module_system:notice:create	\N	\N	\N	\N	\N	f	t	f	公告创建	null	f	17	76	521e80ec-2416-459a-8125-d6821f3f1f1a	0	初始化数据	2026-02-23 06:41:21.173637	2026-02-23 06:41:21.173637
公告修改	3	2	module_system:notice:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	17	77	7981962f-4c0d-4eab-b893-bc160e2e35b3	0	初始化数据	2026-02-23 06:41:21.17364	2026-02-23 06:41:21.17364
公告删除	3	3	module_system:notice:delete	\N	\N	\N	\N	\N	f	t	f	公告删除	null	f	17	78	6a3dffc1-a146-435a-b2c7-4f86d05570b0	0	初始化数据	2026-02-23 06:41:21.173643	2026-02-23 06:41:21.173643
公告导出	3	4	module_system:notice:export	\N	\N	\N	\N	\N	f	t	f	公告导出	null	f	17	79	13d90919-e964-4f5c-8ac0-8f0fbcc80b94	0	初始化数据	2026-02-23 06:41:21.173646	2026-02-23 06:41:21.173646
公告批量修改状态	3	5	module_system:notice:patch	\N	\N	\N	\N	\N	f	t	f	公告批量修改状态	null	f	17	80	14edbcd8-2e89-4ceb-96cb-99f45aed2553	0	初始化数据	2026-02-23 06:41:21.173649	2026-02-23 06:41:21.173649
公告详情	3	6	module_system:notice:detail	\N	\N	\N	\N	\N	f	t	f	公告详情	null	f	17	81	419c3a6c-b2da-4cfd-96b6-689608d198fb	0	初始化数据	2026-02-23 06:41:21.173652	2026-02-23 06:41:21.173652
查询公告	3	5	module_system:notice:query	\N	\N	\N	\N	\N	f	t	f	查询公告	null	f	17	82	339b80bf-add7-4cf2-85d5-88157f6c4ecd	0	初始化数据	2026-02-23 06:41:21.173655	2026-02-23 06:41:21.173655
创建参数	3	1	module_system:param:create	\N	\N	\N	\N	\N	f	t	f	创建参数	null	f	18	83	3ee381e8-4d34-47fa-acb0-34d403623091	0	初始化数据	2026-02-23 06:41:21.173658	2026-02-23 06:41:21.173658
修改参数	3	2	module_system:param:update	\N	\N	\N	\N	\N	f	t	f	修改参数	null	f	18	84	84a567d9-c046-4055-8f9e-3422f57a1e07	0	初始化数据	2026-02-23 06:41:21.173661	2026-02-23 06:41:21.173661
删除参数	3	3	module_system:param:delete	\N	\N	\N	\N	\N	f	t	f	删除参数	null	f	18	85	e221dfb6-cded-4cbe-bb2b-6ee6e2025a6b	0	初始化数据	2026-02-23 06:41:21.173666	2026-02-23 06:41:21.173666
导出参数	3	4	module_system:param:export	\N	\N	\N	\N	\N	f	t	f	导出参数	null	f	18	86	54c9c24c-7eee-4990-9123-d24205027057	0	初始化数据	2026-02-23 06:41:21.173669	2026-02-23 06:41:21.17367
参数上传	3	5	module_system:param:upload	\N	\N	\N	\N	\N	f	t	f	参数上传	null	f	18	87	8330b1f0-ff6a-4b4c-9535-0c8eb6280303	0	初始化数据	2026-02-23 06:41:21.173673	2026-02-23 06:41:21.173673
参数详情	3	6	module_system:param:detail	\N	\N	\N	\N	\N	f	t	f	参数详情	null	f	18	88	7dd00690-edef-4575-88af-c583b488d786	0	初始化数据	2026-02-23 06:41:21.173676	2026-02-23 06:41:21.173676
查询参数	3	7	module_system:param:query	\N	\N	\N	\N	\N	f	t	f	查询参数	null	f	18	89	99e650c6-0c0d-4847-a398-a733a6718e3d	0	初始化数据	2026-02-23 06:41:21.173679	2026-02-23 06:41:21.173679
创建字典类型	3	1	module_system:dict_type:create	\N	\N	\N	\N	\N	f	t	f	创建字典类型	null	f	19	90	095bff6a-eb76-4277-a3d4-a66171d7b974	0	初始化数据	2026-02-23 06:41:21.173682	2026-02-23 06:41:21.173682
修改字典类型	3	2	module_system:dict_type:update	\N	\N	\N	\N	\N	f	t	f	修改字典类型	null	f	19	91	30b1a794-959e-4ae8-a83c-1080a71ea221	0	初始化数据	2026-02-23 06:41:21.173685	2026-02-23 06:41:21.173685
删除字典类型	3	3	module_system:dict_type:delete	\N	\N	\N	\N	\N	f	t	f	删除字典类型	null	f	19	92	1ebcd0e2-c459-4313-864e-4d8d8617abad	0	初始化数据	2026-02-23 06:41:21.173688	2026-02-23 06:41:21.173689
导出字典类型	3	4	module_system:dict_type:export	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	19	93	4083a801-37d5-4492-9caa-a6186545b984	0	初始化数据	2026-02-23 06:41:21.173691	2026-02-23 06:41:21.173692
批量修改字典状态	3	5	module_system:dict_type:patch	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	19	94	eb02426e-b219-47df-b6b9-680a5e71bf26	0	初始化数据	2026-02-23 06:41:21.173694	2026-02-23 06:41:21.173695
字典数据查询	3	6	module_system:dict_data:query	\N	\N	\N	\N	\N	f	t	f	字典数据查询	null	f	19	95	b38fcb32-1802-4ae4-9306-c702f684f261	0	初始化数据	2026-02-23 06:41:21.173697	2026-02-23 06:41:21.173698
创建字典数据	3	7	module_system:dict_data:create	\N	\N	\N	\N	\N	f	t	f	创建字典数据	null	f	19	96	471b6c3b-9228-4f91-afb9-5ad0bc572161	0	初始化数据	2026-02-23 06:41:21.1737	2026-02-23 06:41:21.173701
修改字典数据	3	8	module_system:dict_data:update	\N	\N	\N	\N	\N	f	t	f	修改字典数据	null	f	19	97	66730add-3ad7-42c1-b7ff-f21f1a57e959	0	初始化数据	2026-02-23 06:41:21.173704	2026-02-23 06:41:21.173704
删除字典数据	3	9	module_system:dict_data:delete	\N	\N	\N	\N	\N	f	t	f	删除字典数据	null	f	19	98	779fe83c-b90a-42bb-8a11-c12aea3a1b8f	0	初始化数据	2026-02-23 06:41:21.173707	2026-02-23 06:41:21.173707
导出字典数据	3	10	module_system:dict_data:export	\N	\N	\N	\N	\N	f	t	f	导出字典数据	null	f	19	99	c2e9cf0f-8421-4e71-9b7e-58c72ecab3ea	0	初始化数据	2026-02-23 06:41:21.17371	2026-02-23 06:41:21.17371
批量修改字典数据状态	3	11	module_system:dict_data:patch	\N	\N	\N	\N	\N	f	t	f	批量修改字典数据状态	null	f	19	100	0c101605-6ed7-458e-9821-bdbe361e8a59	0	初始化数据	2026-02-23 06:41:21.173713	2026-02-23 06:41:21.173713
详情字典类型	3	12	module_system:dict_type:detail	\N	\N	\N	\N	\N	f	t	f	详情字典类型	null	f	19	101	c5731311-8f4d-422a-ae10-c3748c367a69	0	初始化数据	2026-02-23 06:41:21.173716	2026-02-23 06:41:21.173716
查询字典类型	3	13	module_system:dict_type:query	\N	\N	\N	\N	\N	f	t	f	查询字典类型	null	f	19	102	3bc26692-ae3a-4436-aa51-af5b43b84584	0	初始化数据	2026-02-23 06:41:21.173719	2026-02-23 06:41:21.173719
详情字典数据	3	14	module_system:dict_data:detail	\N	\N	\N	\N	\N	f	t	f	详情字典数据	null	f	19	103	f8fc6c1c-8a27-4b2f-b4c2-97326370fbf5	0	初始化数据	2026-02-23 06:41:21.173722	2026-02-23 06:41:21.173722
在线用户强制下线	3	1	module_monitor:online:delete	\N	\N	\N	\N	\N	f	t	f	在线用户强制下线	null	f	20	104	d76e74d8-fa99-4402-a32a-0e27b16e1cb0	0	初始化数据	2026-02-23 06:41:21.173725	2026-02-23 06:41:21.173725
清除缓存	3	1	module_monitor:cache:delete	\N	\N	\N	\N	\N	f	t	f	清除缓存	null	f	22	105	a9c6b095-c355-4823-ac36-6d8025328e71	0	初始化数据	2026-02-23 06:41:21.173728	2026-02-23 06:41:21.173728
文件上传	3	1	module_monitor:resource:upload	\N	\N	\N	\N	\N	f	t	f	文件上传	null	f	23	106	3fe31502-38c1-4052-9e40-8ce04ac843a4	0	初始化数据	2026-02-23 06:41:21.173731	2026-02-23 06:41:21.173731
文件下载	3	2	module_monitor:resource:download	\N	\N	\N	\N	\N	f	t	f	文件下载	null	f	23	107	4598946e-e3c8-4467-b880-86b8b2726adc	0	初始化数据	2026-02-23 06:41:21.173734	2026-02-23 06:41:21.173734
文件删除	3	3	module_monitor:resource:delete	\N	\N	\N	\N	\N	f	t	f	文件删除	null	f	23	108	e4cea8eb-5ddd-4f44-a711-367c5d936996	0	初始化数据	2026-02-23 06:41:21.173737	2026-02-23 06:41:21.173737
文件移动	3	4	module_monitor:resource:move	\N	\N	\N	\N	\N	f	t	f	文件移动	null	f	23	109	00601053-5ca0-4d4f-a754-ace07a8b3460	0	初始化数据	2026-02-23 06:41:21.17374	2026-02-23 06:41:21.173741
文件复制	3	5	module_monitor:resource:copy	\N	\N	\N	\N	\N	f	t	f	文件复制	null	f	23	110	4ffc977a-a8e1-4132-818e-861f19ad6d6d	0	初始化数据	2026-02-23 06:41:21.173743	2026-02-23 06:41:21.173744
文件重命名	3	6	module_monitor:resource:rename	\N	\N	\N	\N	\N	f	t	f	文件重命名	null	f	23	111	4b341656-e788-49e6-a2d5-7e0e974bf1da	0	初始化数据	2026-02-23 06:41:21.173746	2026-02-23 06:41:21.173747
创建目录	3	7	module_monitor:resource:create_dir	\N	\N	\N	\N	\N	f	t	f	创建目录	null	f	23	112	0edb9146-f008-4d04-9f56-83a352a205e9	0	初始化数据	2026-02-23 06:41:21.17375	2026-02-23 06:41:21.17375
导出文件列表	3	9	module_monitor:resource:export	\N	\N	\N	\N	\N	f	t	f	导出文件列表	null	f	23	113	768f4d85-56a0-49bf-994a-9f63478fccea	0	初始化数据	2026-02-23 06:41:21.173753	2026-02-23 06:41:21.173753
查询代码生成业务表列表	3	1	module_generator:gencode:query	\N	\N	\N	\N	\N	f	t	f	查询代码生成业务表列表	null	f	27	114	8ca073c8-5aab-40a2-bb79-f8988712f23b	0	查询代码生成业务表列表	2026-02-23 06:41:21.173757	2026-02-23 06:41:21.173758
创建表结构	3	2	module_generator:gencode:create	\N	\N	\N	\N	\N	f	t	f	创建表结构	null	f	27	115	dcc96f93-b3a2-44bf-b60c-7ae80e6150b0	0	创建表结构	2026-02-23 06:41:21.17376	2026-02-23 06:41:21.173761
编辑业务表信息	3	3	module_generator:gencode:update	\N	\N	\N	\N	\N	f	t	f	编辑业务表信息	null	f	27	116	24e6a4b6-0c42-46a4-9248-0fffec5129a8	0	编辑业务表信息	2026-02-23 06:41:21.173763	2026-02-23 06:41:21.173764
删除业务表信息	3	4	module_generator:gencode:delete	\N	\N	\N	\N	\N	f	t	f	删除业务表信息	null	f	27	117	5cac5d12-3b91-4be4-b4de-f53db9ca92fe	0	删除业务表信息	2026-02-23 06:41:21.173766	2026-02-23 06:41:21.173767
导入表结构	3	5	module_generator:gencode:import	\N	\N	\N	\N	\N	f	t	f	导入表结构	null	f	27	118	0851b90e-d310-407a-a308-2577866a91f6	0	导入表结构	2026-02-23 06:41:21.17377	2026-02-23 06:41:21.17377
批量生成代码	3	6	module_generator:gencode:operate	\N	\N	\N	\N	\N	f	t	f	批量生成代码	null	f	27	119	810d7279-44e7-420e-909e-5cfd75e2c86a	0	批量生成代码	2026-02-23 06:41:21.173773	2026-02-23 06:41:21.173773
生成代码到指定路径	3	7	module_generator:gencode:code	\N	\N	\N	\N	\N	f	t	f	生成代码到指定路径	null	f	27	120	9865b103-927a-4f92-b1d5-c39d7500d16f	0	生成代码到指定路径	2026-02-23 06:41:21.173776	2026-02-23 06:41:21.173776
查询数据库表列表	3	8	module_generator:dblist:query	\N	\N	\N	\N	\N	f	t	f	查询数据库表列表	null	f	27	121	c2f14aba-d830-4450-af96-29359d9de993	0	查询数据库表列表	2026-02-23 06:41:21.173779	2026-02-23 06:41:21.173779
同步数据库	3	9	module_generator:db:sync	\N	\N	\N	\N	\N	f	t	f	同步数据库	null	f	27	122	d22e39b2-0979-4d76-8630-a56e4c8854da	0	同步数据库	2026-02-23 06:41:21.173782	2026-02-23 06:41:21.173782
创建应用	3	1	module_application:myapp:create	\N	\N	\N	\N	\N	f	t	f	创建应用	null	f	28	123	bdecb3a3-d65b-470e-b741-d1871324615e	0	初始化数据	2026-02-23 06:41:21.173785	2026-02-23 06:41:21.173785
修改应用	3	2	module_application:myapp:update	\N	\N	\N	\N	\N	f	t	f	修改应用	null	f	28	124	7dd68d38-8def-49e0-be72-25922d7a8269	0	初始化数据	2026-02-23 06:41:21.173788	2026-02-23 06:41:21.173788
删除应用	3	3	module_application:myapp:delete	\N	\N	\N	\N	\N	f	t	f	删除应用	null	f	28	125	8ba51c45-aa9c-417d-8ccc-30b81f226920	0	初始化数据	2026-02-23 06:41:21.173791	2026-02-23 06:41:21.173791
批量修改应用状态	3	4	module_application:myapp:patch	\N	\N	\N	\N	\N	f	t	f	批量修改应用状态	null	f	28	126	e90ed814-d499-499e-8938-8e2d8b2f550e	0	初始化数据	2026-02-23 06:41:21.173794	2026-02-23 06:41:21.173794
详情应用	3	5	module_application:myapp:detail	\N	\N	\N	\N	\N	f	t	f	详情应用	null	f	28	127	4676114a-80ed-436d-aad4-338ddab7dafe	0	初始化数据	2026-02-23 06:41:21.173797	2026-02-23 06:41:21.173797
查询应用	3	6	module_application:myapp:query	\N	\N	\N	\N	\N	f	t	f	查询应用	null	f	28	128	c08e895a-9f3f-478a-9831-3e091cb95541	0	初始化数据	2026-02-23 06:41:21.1738	2026-02-23 06:41:21.1738
会话标题详情	3	1	module_ai:chat_session:detail	\N	\N	\N	\N	\N	f	t	f	会话标题详情	null	f	29	129	0504afd5-fb1f-42ef-9f75-a80df3362fe6	0	会话标题详情	2026-02-23 06:41:21.173803	2026-02-23 06:41:21.173803
创建会话标题	3	2	module_ai:chat_session:create	\N	\N	\N	\N	\N	f	t	f	创建会话标题	null	f	29	130	b4b43f5b-386c-4b98-a9a6-8a5c966b3523	0	创建会话标题	2026-02-23 06:41:21.173806	2026-02-23 06:41:21.173806
修改会话标题	3	3	module_ai:chat_session:update	\N	\N	\N	\N	\N	f	t	f	修改会话标题	null	f	29	131	ca960e47-f12c-4b28-bb64-73bd8e8f4b63	0	修改会话标题	2026-02-23 06:41:21.173809	2026-02-23 06:41:21.17381
删除会话标题	3	4	module_ai:chat_session:delete	\N	\N	\N	\N	\N	f	t	f	删除会话标题	null	f	29	132	3da7d6a5-bc5f-4ba6-8b1c-ed3369ca6b8a	0	删除会话标题	2026-02-23 06:41:21.173812	2026-02-23 06:41:21.173813
查询会话标题	3	5	module_ai:chat_session:query	\N	\N	\N	\N	\N	f	t	f	查询会话标题	null	f	29	133	78e4ac12-f11d-4cb8-8cff-739dc2bb0774	0	查询会话标题	2026-02-23 06:41:21.173815	2026-02-23 06:41:21.173816
会话消息详情	3	6	module_ai:chat_message:detail	\N	\N	\N	\N	\N	f	t	f	会话消息详情	null	f	30	134	579077fa-e8b6-4cf0-b1d6-df12245c5d64	0	会话消息详情	2026-02-23 06:41:21.173818	2026-02-23 06:41:21.173819
创建会话消息	3	7	module_ai:chat_message:create	\N	\N	\N	\N	\N	f	t	f	创建会话消息	null	f	30	135	f6c3a543-8e74-40ba-b5b8-d998b1626cb3	0	创建会话消息	2026-02-23 06:41:21.173821	2026-02-23 06:41:21.173822
修改会话消息	3	8	module_ai:chat_message:update	\N	\N	\N	\N	\N	f	t	f	修改会话消息	null	f	30	136	dd8dbd57-a888-4520-96fd-bacb1f207d58	0	修改会话消息	2026-02-23 06:41:21.173824	2026-02-23 06:41:21.173825
删除会话消息	3	9	module_ai:chat_message:delete	\N	\N	\N	\N	\N	f	t	f	删除会话消息	null	f	30	137	3883db70-c8f9-4522-8e7a-a4ee10c1b4cd	0	删除会话消息	2026-02-23 06:41:21.173827	2026-02-23 06:41:21.173828
查询会话消息	3	10	module_ai:chat_message:query	\N	\N	\N	\N	\N	f	t	f	查询会话消息	null	f	30	138	a920ea5c-cc83-48df-9d8c-a3ed3afe1a75	0	查询会话消息	2026-02-23 06:41:21.17383	2026-02-23 06:41:21.173831
AI对话	3	1	module_ai:chat:ws	\N	\N	\N	\N	\N	f	t	f	AI对话	null	f	31	139	2ea1cc9e-8ef3-40ac-89d4-c293db818542	0	AI对话	2026-02-23 06:41:21.173833	2026-02-23 06:41:21.173834
查询调度器	3	1	module_task:job:query	\N	\N	\N	\N	\N	f	t	f	查询调度器	null	f	32	140	003d0cc2-9eda-47ab-90ca-1309a6b7ffa3	0	查询调度器	2026-02-23 06:41:21.173836	2026-02-23 06:41:21.173837
操作调度器	3	2	module_task:job:update	\N	\N	\N	\N	\N	f	t	f	操作调度器	null	f	32	141	b9789751-9f6c-4258-96ad-3ab7adb1f51c	0	操作调度器	2026-02-23 06:41:21.17384	2026-02-23 06:41:21.17384
删除执行日志	3	3	module_task:job:delete	\N	\N	\N	\N	\N	f	t	f	删除执行日志	null	f	32	142	aa780ddc-5f13-426f-9095-244f4571d2ac	0	删除执行日志	2026-02-23 06:41:21.173843	2026-02-23 06:41:21.173843
详情执行日志	3	4	module_task:job:detail	\N	\N	\N	\N	\N	f	t	f	详情执行日志	null	f	32	143	3bc0d878-39f4-4101-9c83-6c8d5ef1aa19	0	详情执行日志	2026-02-23 06:41:21.173846	2026-02-23 06:41:21.173846
创建节点	3	1	module_task:node:create	\N	\N	\N	\N	\N	f	t	f	创建节点	null	f	33	144	f32cadf5-1777-409a-a69f-860ab2d36643	0	创建节点	2026-02-23 06:41:21.173849	2026-02-23 06:41:21.173849
修改节点	3	2	module_task:node:update	\N	\N	\N	\N	\N	f	t	f	修改节点	null	f	33	145	63a99915-d1ef-455e-8441-56cca1ac8079	0	修改节点	2026-02-23 06:41:21.173852	2026-02-23 06:41:21.173852
删除节点	3	3	module_task:node:delete	\N	\N	\N	\N	\N	f	t	f	删除节点	null	f	33	146	d5fabe64-b599-440c-bfc8-d6f73248f820	0	删除节点	2026-02-23 06:41:21.173855	2026-02-23 06:41:21.173855
详情节点	3	4	module_task:node:detail	\N	\N	\N	\N	\N	f	t	f	详情节点	null	f	33	147	7ed7c0ac-f804-4dd5-ba0d-d926e43d10e1	0	详情节点	2026-02-23 06:41:21.173858	2026-02-23 06:41:21.173858
查询节点	3	5	module_task:node:query	\N	\N	\N	\N	\N	f	t	f	查询节点	null	f	33	148	261d60b6-e6ef-4e73-b0d3-56848fe23ba7	0	查询节点	2026-02-23 06:41:21.173861	2026-02-23 06:41:21.173861
创建工作流	3	1	module_task:workflow:create	\N	\N	\N	\N	\N	f	t	f	创建工作流	null	f	34	149	80ee4f30-151a-4753-8110-9b7a2b05a753	0	创建工作流	2026-02-23 06:41:21.173864	2026-02-23 06:41:21.173864
修改工作流	3	2	module_task:workflow:update	\N	\N	\N	\N	\N	f	t	f	修改工作流	null	f	34	150	54795961-3a31-4f75-a643-194c4b149849	0	修改工作流	2026-02-23 06:41:21.173867	2026-02-23 06:41:21.173867
删除工作流	3	3	module_task:workflow:delete	\N	\N	\N	\N	\N	f	t	f	删除工作流	null	f	34	151	93e6b6c2-a1b3-491f-9680-4514f4eb1903	0	删除工作流	2026-02-23 06:41:21.17387	2026-02-23 06:41:21.17387
发布工作流	3	4	module_task:workflow:publish	\N	\N	\N	\N	\N	f	t	f	发布工作流	null	f	34	152	87a085cb-a286-497b-b5f3-e0bee372ca04	0	发布工作流	2026-02-23 06:41:21.173873	2026-02-23 06:41:21.173873
执行工作流	3	5	module_task:workflow:execute	\N	\N	\N	\N	\N	f	t	f	执行工作流	null	f	34	153	441d4955-54eb-437f-a013-c8bd855e0bf1	0	执行工作流	2026-02-23 06:41:21.173876	2026-02-23 06:41:21.173876
详情工作流	3	6	module_task:workflow:detail	\N	\N	\N	\N	\N	f	t	f	详情工作流	null	f	34	154	74b85684-55b2-4150-82c7-6d5385bd1c97	0	详情工作流	2026-02-23 06:41:21.173879	2026-02-23 06:41:21.173879
查询工作流	3	7	module_task:workflow:query	\N	\N	\N	\N	\N	f	t	f	查询工作流	null	f	34	155	53b2a139-6fc8-4c97-ac08-c4cc1dee8ba2	0	查询工作流	2026-02-23 06:41:21.173882	2026-02-23 06:41:21.173882
创建示例	3	1	module_example:demo:create	\N	\N	\N	\N	\N	f	t	f	创建示例	null	f	35	156	b9f9fc27-4408-4720-a913-e104444cc0e4	0	初始化数据	2026-02-23 06:41:21.173885	2026-02-23 06:41:21.173885
更新示例	3	2	module_example:demo:update	\N	\N	\N	\N	\N	f	t	f	更新示例	null	f	35	157	f981c798-5087-4289-ad0a-8d3d2e4bbb9f	0	初始化数据	2026-02-23 06:41:21.173888	2026-02-23 06:41:21.173888
删除示例	3	3	module_example:demo:delete	\N	\N	\N	\N	\N	f	t	f	删除示例	null	f	35	158	15256819-e11c-4352-98ed-f37615b6b972	0	初始化数据	2026-02-23 06:41:21.173891	2026-02-23 06:41:21.173891
批量修改示例状态	3	4	module_example:demo:patch	\N	\N	\N	\N	\N	f	t	f	批量修改示例状态	null	f	35	159	ae5b1a91-6cc0-4b40-9c50-d1034f805de8	0	初始化数据	2026-02-23 06:41:21.173894	2026-02-23 06:41:21.173895
导出示例	3	5	module_example:demo:export	\N	\N	\N	\N	\N	f	t	f	导出示例	null	f	35	160	c5f63630-2543-4463-990d-7fa91c2e82a4	0	初始化数据	2026-02-23 06:41:21.173897	2026-02-23 06:41:21.173898
导入示例	3	6	module_example:demo:import	\N	\N	\N	\N	\N	f	t	f	导入示例	null	f	35	161	9c12d2e8-809d-4749-b3c6-5ee666edc678	0	初始化数据	2026-02-23 06:41:21.173903	2026-02-23 06:41:21.173903
下载导入示例模版	3	7	module_example:demo:download	\N	\N	\N	\N	\N	f	t	f	下载导入示例模版	null	f	35	162	eae1f136-ec1c-4895-812c-33e9ef13e88c	0	初始化数据	2026-02-23 06:41:21.173907	2026-02-23 06:41:21.173907
详情示例	3	8	module_example:demo:detail	\N	\N	\N	\N	\N	f	t	f	详情示例	null	f	35	163	f9abb4ab-fab3-4e01-b52f-de3172dcbcb0	0	初始化数据	2026-02-23 06:41:21.173911	2026-02-23 06:41:21.173911
查询示例	3	9	module_example:demo:query	\N	\N	\N	\N	\N	f	t	f	查询示例	null	f	35	164	7a782c5e-6725-499f-9de4-ce27470fca06	0	初始化数据	2026-02-23 06:41:21.173915	2026-02-23 06:41:21.173915
\.


--
-- Data for Name: sys_notice; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_notice (notice_title, notice_type, notice_content, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_param; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_param (config_name, config_key, config_value, config_type, id, uuid, status, description, created_time, updated_time) FROM stdin;
网站名称	sys_web_title	FastApiAdmin	t	1	689c9ec6-ac80-40bd-92a3-4479a9168210	0	初始化数据	2026-02-23 06:41:21.182814	2026-02-23 06:41:21.182815
网站描述	sys_web_description	FastApiAdmin 是完全开源的权限管理系统	t	2	dd8aaae7-9d59-48e7-99a8-514c8d954ef7	0	初始化数据	2026-02-23 06:41:21.182819	2026-02-23 06:41:21.182819
网页图标	sys_web_favicon	https://service.fastapiadmin.com/api/v1/static/image/favicon.png	t	3	2c5b11ff-0d1c-42eb-a0f6-727aecdba49b	0	初始化数据	2026-02-23 06:41:21.182822	2026-02-23 06:41:21.182823
网站Logo	sys_web_logo	https://service.fastapiadmin.com/api/v1/static/image/logo.png	t	4	d5370fad-d85a-4e35-bda9-f554c640c2a3	0	初始化数据	2026-02-23 06:41:21.182826	2026-02-23 06:41:21.182826
登录背景	sys_login_background	https://service.fastapiadmin.com/api/v1/static/image/background.svg	t	5	a7413027-0d73-48ce-9424-0554e8a90c71	0	初始化数据	2026-02-23 06:41:21.182829	2026-02-23 06:41:21.18283
版权信息	sys_web_copyright	Copyright © 2025-2026 service.fastapiadmin.com 版权所有	t	6	a6f89081-0d20-4afb-9109-a01cac6d2d36	0	初始化数据	2026-02-23 06:41:21.182832	2026-02-23 06:41:21.182833
备案信息	sys_keep_record	陕ICP备2025069493号-1	t	7	510dbf53-156c-40bb-86dd-7e488936380c	0	初始化数据	2026-02-23 06:41:21.182836	2026-02-23 06:41:21.182836
帮助文档	sys_help_doc	https://service.fastapiadmin.com	t	8	81809551-4a81-4d72-a1df-f507420db2db	0	初始化数据	2026-02-23 06:41:21.182839	2026-02-23 06:41:21.182839
隐私政策	sys_web_privacy	https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE	t	9	a14f2130-1d69-4d68-9adb-048200ec3776	0	初始化数据	2026-02-23 06:41:21.182842	2026-02-23 06:41:21.182842
用户协议	sys_web_clause	https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE	t	10	a616befc-27f4-4527-9b58-71b41fe47349	0	初始化数据	2026-02-23 06:41:21.182845	2026-02-23 06:41:21.182846
源码代码	sys_git_code	https://github.com/fastapiadmin/FastapiAdmin.git	t	11	cb6ebc7c-482f-4d02-83bd-4e64308adf9d	0	初始化数据	2026-02-23 06:41:21.182848	2026-02-23 06:41:21.182849
项目版本	sys_web_version	2.0.0	t	12	21486851-cb1d-407b-869c-856ef9770ef0	0	初始化数据	2026-02-23 06:41:21.182852	2026-02-23 06:41:21.182852
演示模式启用	demo_enable	false	t	13	8e8b94a5-1ed4-489a-b2af-7c2d926ddb76	0	初始化数据	2026-02-23 06:41:21.182855	2026-02-23 06:41:21.182855
演示访问IP白名单	ip_white_list	["127.0.0.1"]	t	14	8a48f730-5772-491e-ab85-45965d0d3407	0	初始化数据	2026-02-23 06:41:21.182858	2026-02-23 06:41:21.182858
接口白名单	white_api_list_path	["/api/v1/system/auth/login", "/api/v1/system/auth/token/refresh", "/api/v1/system/auth/captcha/get", "/api/v1/system/auth/logout", "/api/v1/system/config/info", "/api/v1/system/user/current/info", "/api/v1/system/notice/available"]	t	15	9bed5906-3d3a-4e24-81f6-b94d6a159d61	0	初始化数据	2026-02-23 06:41:21.182861	2026-02-23 06:41:21.182862
访问IP黑名单	ip_black_list	[]	t	16	3b4fe81d-fc26-48bb-b500-4f802a822f29	0	初始化数据	2026-02-23 06:41:21.182864	2026-02-23 06:41:21.182865
\.


--
-- Data for Name: sys_position; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_position (name, "order", id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_role; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_role (name, code, "order", data_scope, id, uuid, status, description, created_time, updated_time) FROM stdin;
管理员角色	ADMIN	1	4	1	3cca130b-aa06-4e38-8895-aac12a824070	0	初始化角色	2026-02-23 06:41:21.187915	2026-02-23 06:41:21.187916
\.


--
-- Data for Name: sys_role_depts; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_role_depts (role_id, dept_id) FROM stdin;
\.


--
-- Data for Name: sys_role_menus; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_role_menus (role_id, menu_id) FROM stdin;
\.


--
-- Data for Name: sys_user; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_user (username, password, name, mobile, email, gender, avatar, is_superuser, last_login, gitee_login, github_login, wx_login, qq_login, dept_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
admin	$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa	超级管理员	\N	\N	0	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	t	\N	\N	\N	\N	\N	1	1	c99f43f6-649f-453d-bbc9-70e4b077841d	0	超级管理员	2026-02-23 06:41:21.200174	2026-02-23 06:41:21.200175	\N	\N
\.


--
-- Data for Name: sys_user_positions; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_user_positions (user_id, position_id) FROM stdin;
\.


--
-- Data for Name: sys_user_roles; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_user_roles (user_id, role_id) FROM stdin;
1	1
\.


--
-- Data for Name: task_job; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.task_job (job_id, job_name, trigger_type, status, next_run_time, job_state, result, error, id, uuid, description, created_time, updated_time) FROM stdin;
\.


--
-- Data for Name: task_node; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.task_node (name, code, category, jobstore, executor, trigger, trigger_args, func, args, kwargs, "coalesce", max_instances, start_date, end_date, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: task_workflow; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.task_workflow (name, code, status, nodes, edges, id, uuid, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Name: ai_chat_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.ai_chat_message_id_seq', 1, false);


--
-- Name: ai_chat_session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.ai_chat_session_id_seq', 1, false);


--
-- Name: app_myapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.app_myapp_id_seq', 1, false);


--
-- Name: gen_demo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_demo_id_seq', 1, false);


--
-- Name: gen_table_column_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_table_column_id_seq', 1, false);


--
-- Name: gen_table_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_table_id_seq', 1, false);


--
-- Name: sys_dept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_dept_id_seq', 1, true);


--
-- Name: sys_dict_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_dict_data_id_seq', 34, true);


--
-- Name: sys_dict_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_dict_type_id_seq', 10, true);


--
-- Name: sys_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_log_id_seq', 1, false);


--
-- Name: sys_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_menu_id_seq', 164, true);


--
-- Name: sys_notice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_notice_id_seq', 1, false);


--
-- Name: sys_param_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_param_id_seq', 16, true);


--
-- Name: sys_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_position_id_seq', 1, false);


--
-- Name: sys_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_role_id_seq', 1, true);


--
-- Name: sys_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_user_id_seq', 1, true);


--
-- Name: task_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.task_job_id_seq', 1, false);


--
-- Name: task_node_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.task_node_id_seq', 1, false);


--
-- Name: task_workflow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.task_workflow_id_seq', 1, false);


--
-- Name: ai_chat_message ai_chat_message_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.ai_chat_message
    ADD CONSTRAINT ai_chat_message_pkey PRIMARY KEY (id);


--
-- Name: ai_chat_session ai_chat_session_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.ai_chat_session
    ADD CONSTRAINT ai_chat_session_pkey PRIMARY KEY (id);


--
-- Name: app_myapp app_myapp_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_myapp
    ADD CONSTRAINT app_myapp_pkey PRIMARY KEY (id);


--
-- Name: apscheduler_jobs apscheduler_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.apscheduler_jobs
    ADD CONSTRAINT apscheduler_jobs_pkey PRIMARY KEY (id);


--
-- Name: gen_demo gen_demo_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_demo
    ADD CONSTRAINT gen_demo_pkey PRIMARY KEY (id);


--
-- Name: gen_table_column gen_table_column_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_pkey PRIMARY KEY (id);


--
-- Name: gen_table gen_table_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_pkey PRIMARY KEY (id);


--
-- Name: sys_dept sys_dept_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_pkey PRIMARY KEY (id);


--
-- Name: sys_dict_data sys_dict_data_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_pkey PRIMARY KEY (id);


--
-- Name: sys_dict_type sys_dict_type_dict_type_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_type
    ADD CONSTRAINT sys_dict_type_dict_type_key UNIQUE (dict_type);


--
-- Name: sys_dict_type sys_dict_type_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_type
    ADD CONSTRAINT sys_dict_type_pkey PRIMARY KEY (id);


--
-- Name: sys_log sys_log_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_pkey PRIMARY KEY (id);


--
-- Name: sys_menu sys_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_menu
    ADD CONSTRAINT sys_menu_pkey PRIMARY KEY (id);


--
-- Name: sys_notice sys_notice_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_pkey PRIMARY KEY (id);


--
-- Name: sys_param sys_param_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_param
    ADD CONSTRAINT sys_param_pkey PRIMARY KEY (id);


--
-- Name: sys_position sys_position_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_pkey PRIMARY KEY (id);


--
-- Name: sys_role_depts sys_role_depts_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_depts
    ADD CONSTRAINT sys_role_depts_pkey PRIMARY KEY (role_id, dept_id);


--
-- Name: sys_role_menus sys_role_menus_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_menus
    ADD CONSTRAINT sys_role_menus_pkey PRIMARY KEY (role_id, menu_id);


--
-- Name: sys_role sys_role_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role
    ADD CONSTRAINT sys_role_pkey PRIMARY KEY (id);


--
-- Name: sys_user sys_user_email_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_email_key UNIQUE (email);


--
-- Name: sys_user sys_user_mobile_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_mobile_key UNIQUE (mobile);


--
-- Name: sys_user sys_user_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_pkey PRIMARY KEY (id);


--
-- Name: sys_user_positions sys_user_positions_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_positions
    ADD CONSTRAINT sys_user_positions_pkey PRIMARY KEY (user_id, position_id);


--
-- Name: sys_user_roles sys_user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_roles
    ADD CONSTRAINT sys_user_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: sys_user sys_user_username_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_username_key UNIQUE (username);


--
-- Name: task_job task_job_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_job
    ADD CONSTRAINT task_job_pkey PRIMARY KEY (id);


--
-- Name: task_node task_node_code_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_code_key UNIQUE (code);


--
-- Name: task_node task_node_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_pkey PRIMARY KEY (id);


--
-- Name: task_workflow task_workflow_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT task_workflow_pkey PRIMARY KEY (id);


--
-- Name: ix_ai_chat_message_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_message_created_time ON public.ai_chat_message USING btree (created_time);


--
-- Name: ix_ai_chat_message_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_message_id ON public.ai_chat_message USING btree (id);


--
-- Name: ix_ai_chat_message_session_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_message_session_id ON public.ai_chat_message USING btree (session_id);


--
-- Name: ix_ai_chat_message_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_message_status ON public.ai_chat_message USING btree (status);


--
-- Name: ix_ai_chat_message_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_message_updated_time ON public.ai_chat_message USING btree (updated_time);


--
-- Name: ix_ai_chat_message_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_ai_chat_message_uuid ON public.ai_chat_message USING btree (uuid);


--
-- Name: ix_ai_chat_session_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_session_created_id ON public.ai_chat_session USING btree (created_id);


--
-- Name: ix_ai_chat_session_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_session_created_time ON public.ai_chat_session USING btree (created_time);


--
-- Name: ix_ai_chat_session_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_session_id ON public.ai_chat_session USING btree (id);


--
-- Name: ix_ai_chat_session_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_session_status ON public.ai_chat_session USING btree (status);


--
-- Name: ix_ai_chat_session_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_session_updated_id ON public.ai_chat_session USING btree (updated_id);


--
-- Name: ix_ai_chat_session_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_chat_session_updated_time ON public.ai_chat_session USING btree (updated_time);


--
-- Name: ix_ai_chat_session_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_ai_chat_session_uuid ON public.ai_chat_session USING btree (uuid);


--
-- Name: ix_app_myapp_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_created_id ON public.app_myapp USING btree (created_id);


--
-- Name: ix_app_myapp_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_created_time ON public.app_myapp USING btree (created_time);


--
-- Name: ix_app_myapp_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_id ON public.app_myapp USING btree (id);


--
-- Name: ix_app_myapp_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_status ON public.app_myapp USING btree (status);


--
-- Name: ix_app_myapp_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_updated_id ON public.app_myapp USING btree (updated_id);


--
-- Name: ix_app_myapp_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_updated_time ON public.app_myapp USING btree (updated_time);


--
-- Name: ix_app_myapp_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_app_myapp_uuid ON public.app_myapp USING btree (uuid);


--
-- Name: ix_apscheduler_jobs_next_run_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_apscheduler_jobs_next_run_time ON public.apscheduler_jobs USING btree (next_run_time);


--
-- Name: ix_gen_demo_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_created_id ON public.gen_demo USING btree (created_id);


--
-- Name: ix_gen_demo_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_created_time ON public.gen_demo USING btree (created_time);


--
-- Name: ix_gen_demo_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_id ON public.gen_demo USING btree (id);


--
-- Name: ix_gen_demo_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_status ON public.gen_demo USING btree (status);


--
-- Name: ix_gen_demo_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_updated_id ON public.gen_demo USING btree (updated_id);


--
-- Name: ix_gen_demo_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_updated_time ON public.gen_demo USING btree (updated_time);


--
-- Name: ix_gen_demo_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_gen_demo_uuid ON public.gen_demo USING btree (uuid);


--
-- Name: ix_gen_table_column_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_created_id ON public.gen_table_column USING btree (created_id);


--
-- Name: ix_gen_table_column_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_created_time ON public.gen_table_column USING btree (created_time);


--
-- Name: ix_gen_table_column_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_id ON public.gen_table_column USING btree (id);


--
-- Name: ix_gen_table_column_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_status ON public.gen_table_column USING btree (status);


--
-- Name: ix_gen_table_column_table_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_table_id ON public.gen_table_column USING btree (table_id);


--
-- Name: ix_gen_table_column_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_updated_id ON public.gen_table_column USING btree (updated_id);


--
-- Name: ix_gen_table_column_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_updated_time ON public.gen_table_column USING btree (updated_time);


--
-- Name: ix_gen_table_column_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_gen_table_column_uuid ON public.gen_table_column USING btree (uuid);


--
-- Name: ix_gen_table_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_created_id ON public.gen_table USING btree (created_id);


--
-- Name: ix_gen_table_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_created_time ON public.gen_table USING btree (created_time);


--
-- Name: ix_gen_table_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_id ON public.gen_table USING btree (id);


--
-- Name: ix_gen_table_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_status ON public.gen_table USING btree (status);


--
-- Name: ix_gen_table_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_updated_id ON public.gen_table USING btree (updated_id);


--
-- Name: ix_gen_table_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_updated_time ON public.gen_table USING btree (updated_time);


--
-- Name: ix_gen_table_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_gen_table_uuid ON public.gen_table USING btree (uuid);


--
-- Name: ix_sys_dept_code; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_code ON public.sys_dept USING btree (code);


--
-- Name: ix_sys_dept_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_created_time ON public.sys_dept USING btree (created_time);


--
-- Name: ix_sys_dept_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_id ON public.sys_dept USING btree (id);


--
-- Name: ix_sys_dept_parent_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_parent_id ON public.sys_dept USING btree (parent_id);


--
-- Name: ix_sys_dept_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_status ON public.sys_dept USING btree (status);


--
-- Name: ix_sys_dept_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_updated_time ON public.sys_dept USING btree (updated_time);


--
-- Name: ix_sys_dept_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_dept_uuid ON public.sys_dept USING btree (uuid);


--
-- Name: ix_sys_dict_data_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_data_created_time ON public.sys_dict_data USING btree (created_time);


--
-- Name: ix_sys_dict_data_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_data_id ON public.sys_dict_data USING btree (id);


--
-- Name: ix_sys_dict_data_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_data_status ON public.sys_dict_data USING btree (status);


--
-- Name: ix_sys_dict_data_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_data_updated_time ON public.sys_dict_data USING btree (updated_time);


--
-- Name: ix_sys_dict_data_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_dict_data_uuid ON public.sys_dict_data USING btree (uuid);


--
-- Name: ix_sys_dict_type_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_type_created_time ON public.sys_dict_type USING btree (created_time);


--
-- Name: ix_sys_dict_type_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_type_id ON public.sys_dict_type USING btree (id);


--
-- Name: ix_sys_dict_type_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_type_status ON public.sys_dict_type USING btree (status);


--
-- Name: ix_sys_dict_type_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_type_updated_time ON public.sys_dict_type USING btree (updated_time);


--
-- Name: ix_sys_dict_type_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_dict_type_uuid ON public.sys_dict_type USING btree (uuid);


--
-- Name: ix_sys_log_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_created_id ON public.sys_log USING btree (created_id);


--
-- Name: ix_sys_log_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_created_time ON public.sys_log USING btree (created_time);


--
-- Name: ix_sys_log_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_id ON public.sys_log USING btree (id);


--
-- Name: ix_sys_log_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_status ON public.sys_log USING btree (status);


--
-- Name: ix_sys_log_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_updated_id ON public.sys_log USING btree (updated_id);


--
-- Name: ix_sys_log_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_updated_time ON public.sys_log USING btree (updated_time);


--
-- Name: ix_sys_log_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_log_uuid ON public.sys_log USING btree (uuid);


--
-- Name: ix_sys_menu_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_created_time ON public.sys_menu USING btree (created_time);


--
-- Name: ix_sys_menu_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_id ON public.sys_menu USING btree (id);


--
-- Name: ix_sys_menu_parent_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_parent_id ON public.sys_menu USING btree (parent_id);


--
-- Name: ix_sys_menu_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_status ON public.sys_menu USING btree (status);


--
-- Name: ix_sys_menu_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_updated_time ON public.sys_menu USING btree (updated_time);


--
-- Name: ix_sys_menu_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_menu_uuid ON public.sys_menu USING btree (uuid);


--
-- Name: ix_sys_notice_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_created_id ON public.sys_notice USING btree (created_id);


--
-- Name: ix_sys_notice_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_created_time ON public.sys_notice USING btree (created_time);


--
-- Name: ix_sys_notice_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_id ON public.sys_notice USING btree (id);


--
-- Name: ix_sys_notice_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_status ON public.sys_notice USING btree (status);


--
-- Name: ix_sys_notice_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_updated_id ON public.sys_notice USING btree (updated_id);


--
-- Name: ix_sys_notice_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_updated_time ON public.sys_notice USING btree (updated_time);


--
-- Name: ix_sys_notice_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_notice_uuid ON public.sys_notice USING btree (uuid);


--
-- Name: ix_sys_param_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_param_created_time ON public.sys_param USING btree (created_time);


--
-- Name: ix_sys_param_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_param_id ON public.sys_param USING btree (id);


--
-- Name: ix_sys_param_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_param_status ON public.sys_param USING btree (status);


--
-- Name: ix_sys_param_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_param_updated_time ON public.sys_param USING btree (updated_time);


--
-- Name: ix_sys_param_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_param_uuid ON public.sys_param USING btree (uuid);


--
-- Name: ix_sys_position_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_created_id ON public.sys_position USING btree (created_id);


--
-- Name: ix_sys_position_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_created_time ON public.sys_position USING btree (created_time);


--
-- Name: ix_sys_position_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_id ON public.sys_position USING btree (id);


--
-- Name: ix_sys_position_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_status ON public.sys_position USING btree (status);


--
-- Name: ix_sys_position_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_updated_id ON public.sys_position USING btree (updated_id);


--
-- Name: ix_sys_position_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_updated_time ON public.sys_position USING btree (updated_time);


--
-- Name: ix_sys_position_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_position_uuid ON public.sys_position USING btree (uuid);


--
-- Name: ix_sys_role_code; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_code ON public.sys_role USING btree (code);


--
-- Name: ix_sys_role_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_created_time ON public.sys_role USING btree (created_time);


--
-- Name: ix_sys_role_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_id ON public.sys_role USING btree (id);


--
-- Name: ix_sys_role_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_status ON public.sys_role USING btree (status);


--
-- Name: ix_sys_role_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_updated_time ON public.sys_role USING btree (updated_time);


--
-- Name: ix_sys_role_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_role_uuid ON public.sys_role USING btree (uuid);


--
-- Name: ix_sys_user_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_created_id ON public.sys_user USING btree (created_id);


--
-- Name: ix_sys_user_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_created_time ON public.sys_user USING btree (created_time);


--
-- Name: ix_sys_user_dept_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_dept_id ON public.sys_user USING btree (dept_id);


--
-- Name: ix_sys_user_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_id ON public.sys_user USING btree (id);


--
-- Name: ix_sys_user_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_status ON public.sys_user USING btree (status);


--
-- Name: ix_sys_user_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_updated_id ON public.sys_user USING btree (updated_id);


--
-- Name: ix_sys_user_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_updated_time ON public.sys_user USING btree (updated_time);


--
-- Name: ix_sys_user_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_user_uuid ON public.sys_user USING btree (uuid);


--
-- Name: ix_task_job_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_job_created_time ON public.task_job USING btree (created_time);


--
-- Name: ix_task_job_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_job_id ON public.task_job USING btree (id);


--
-- Name: ix_task_job_job_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_job_job_id ON public.task_job USING btree (job_id);


--
-- Name: ix_task_job_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_job_updated_time ON public.task_job USING btree (updated_time);


--
-- Name: ix_task_job_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_task_job_uuid ON public.task_job USING btree (uuid);


--
-- Name: ix_task_node_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_node_created_id ON public.task_node USING btree (created_id);


--
-- Name: ix_task_node_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_node_created_time ON public.task_node USING btree (created_time);


--
-- Name: ix_task_node_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_node_id ON public.task_node USING btree (id);


--
-- Name: ix_task_node_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_node_status ON public.task_node USING btree (status);


--
-- Name: ix_task_node_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_node_updated_id ON public.task_node USING btree (updated_id);


--
-- Name: ix_task_node_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_node_updated_time ON public.task_node USING btree (updated_time);


--
-- Name: ix_task_node_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_task_node_uuid ON public.task_node USING btree (uuid);


--
-- Name: ix_task_workflow_code; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_task_workflow_code ON public.task_workflow USING btree (code);


--
-- Name: ix_task_workflow_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_workflow_created_id ON public.task_workflow USING btree (created_id);


--
-- Name: ix_task_workflow_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_workflow_created_time ON public.task_workflow USING btree (created_time);


--
-- Name: ix_task_workflow_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_workflow_id ON public.task_workflow USING btree (id);


--
-- Name: ix_task_workflow_name; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_workflow_name ON public.task_workflow USING btree (name);


--
-- Name: ix_task_workflow_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_workflow_status ON public.task_workflow USING btree (status);


--
-- Name: ix_task_workflow_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_workflow_updated_id ON public.task_workflow USING btree (updated_id);


--
-- Name: ix_task_workflow_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_task_workflow_updated_time ON public.task_workflow USING btree (updated_time);


--
-- Name: ix_task_workflow_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_task_workflow_uuid ON public.task_workflow USING btree (uuid);


--
-- Name: ai_chat_message ai_chat_message_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.ai_chat_message
    ADD CONSTRAINT ai_chat_message_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.ai_chat_session(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ai_chat_session ai_chat_session_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.ai_chat_session
    ADD CONSTRAINT ai_chat_session_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ai_chat_session ai_chat_session_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.ai_chat_session
    ADD CONSTRAINT ai_chat_session_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_myapp app_myapp_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_myapp
    ADD CONSTRAINT app_myapp_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_myapp app_myapp_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_myapp
    ADD CONSTRAINT app_myapp_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_demo gen_demo_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_demo
    ADD CONSTRAINT gen_demo_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_demo gen_demo_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_demo
    ADD CONSTRAINT gen_demo_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table_column gen_table_column_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table_column gen_table_column_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.gen_table(id) ON DELETE CASCADE;


--
-- Name: gen_table_column gen_table_column_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table gen_table_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table gen_table_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dept sys_dept_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.sys_dept(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dict_data sys_dict_data_dict_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_dict_type_id_fkey FOREIGN KEY (dict_type_id) REFERENCES public.sys_dict_type(id) ON DELETE CASCADE;


--
-- Name: sys_log sys_log_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_log sys_log_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_menu sys_menu_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_menu
    ADD CONSTRAINT sys_menu_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.sys_menu(id) ON DELETE SET NULL;


--
-- Name: sys_notice sys_notice_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_notice sys_notice_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_position sys_position_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_position sys_position_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_role_depts sys_role_depts_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_depts
    ADD CONSTRAINT sys_role_depts_dept_id_fkey FOREIGN KEY (dept_id) REFERENCES public.sys_dept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role_depts sys_role_depts_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_depts
    ADD CONSTRAINT sys_role_depts_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.sys_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role_menus sys_role_menus_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_menus
    ADD CONSTRAINT sys_role_menus_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.sys_menu(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role_menus sys_role_menus_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_menus
    ADD CONSTRAINT sys_role_menus_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.sys_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user sys_user_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_user sys_user_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_dept_id_fkey FOREIGN KEY (dept_id) REFERENCES public.sys_dept(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_user_positions sys_user_positions_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_positions
    ADD CONSTRAINT sys_user_positions_position_id_fkey FOREIGN KEY (position_id) REFERENCES public.sys_position(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user_positions sys_user_positions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_positions
    ADD CONSTRAINT sys_user_positions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user_roles sys_user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_roles
    ADD CONSTRAINT sys_user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.sys_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user_roles sys_user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_roles
    ADD CONSTRAINT sys_user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user sys_user_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_node task_node_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_node task_node_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_workflow task_workflow_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT task_workflow_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_workflow task_workflow_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT task_workflow_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

\unrestrict ulNIgdx7CtT5MrgK5O5igyKTPSLK56cbbdePKwjuQbUm20ekyjOAhWcXtSxiDc6

