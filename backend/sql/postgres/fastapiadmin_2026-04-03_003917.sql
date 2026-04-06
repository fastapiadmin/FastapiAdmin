--
-- PostgreSQL database dump
--

\restrict ZPSb5Q9rvfnfbn6VdXJ2edWyHcIou9jw4hZaoDETBqBWj7T0xI08ijcpb6b4BKi

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
-- Name: ai; Type: SCHEMA; Schema: -; Owner: root
--

CREATE SCHEMA ai;


ALTER SCHEMA ai OWNER TO root;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agno_schema_versions; Type: TABLE; Schema: ai; Owner: root
--

CREATE TABLE ai.agno_schema_versions (
    table_name character varying NOT NULL,
    version character varying NOT NULL,
    created_at character varying NOT NULL,
    updated_at character varying
);


ALTER TABLE ai.agno_schema_versions OWNER TO root;

--
-- Name: agno_sessions; Type: TABLE; Schema: ai; Owner: root
--

CREATE TABLE ai.agno_sessions (
    session_id character varying NOT NULL,
    session_type character varying NOT NULL,
    agent_id character varying,
    team_id character varying,
    workflow_id character varying,
    user_id character varying,
    session_data jsonb,
    agent_data jsonb,
    team_data jsonb,
    workflow_data jsonb,
    metadata jsonb,
    runs jsonb,
    summary jsonb,
    created_at bigint NOT NULL,
    updated_at bigint
);


ALTER TABLE ai.agno_sessions OWNER TO root;

--
-- Name: app_portal; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.app_portal (
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


ALTER TABLE public.app_portal OWNER TO root;

--
-- Name: TABLE app_portal; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.app_portal IS '门户应用登记';


--
-- Name: COLUMN app_portal.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.name IS '应用名称';


--
-- Name: COLUMN app_portal.access_url; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.access_url IS '访问地址';


--
-- Name: COLUMN app_portal.icon_url; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.icon_url IS '应用图标URL';


--
-- Name: COLUMN app_portal.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.id IS '主键ID';


--
-- Name: COLUMN app_portal.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN app_portal.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN app_portal.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.description IS '备注/描述';


--
-- Name: COLUMN app_portal.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.created_time IS '创建时间';


--
-- Name: COLUMN app_portal.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.updated_time IS '更新时间';


--
-- Name: COLUMN app_portal.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.created_id IS '创建人ID';


--
-- Name: COLUMN app_portal.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.updated_id IS '更新人ID';


--
-- Name: app_portal_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.app_portal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.app_portal_id_seq OWNER TO root;

--
-- Name: app_portal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.app_portal_id_seq OWNED BY public.app_portal.id;


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
-- Name: gen_demo; Type: TABLE; Schema: public; Owner: root
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


ALTER TABLE public.gen_demo OWNER TO root;

--
-- Name: TABLE gen_demo; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.gen_demo IS '示例表';


--
-- Name: COLUMN gen_demo.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.name IS '名称';


--
-- Name: COLUMN gen_demo.a; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.a IS '整数';


--
-- Name: COLUMN gen_demo.b; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.b IS '大整数';


--
-- Name: COLUMN gen_demo.c; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.c IS '浮点数';


--
-- Name: COLUMN gen_demo.d; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.d IS '布尔型';


--
-- Name: COLUMN gen_demo.e; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.e IS '日期';


--
-- Name: COLUMN gen_demo.f; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.f IS '时间';


--
-- Name: COLUMN gen_demo.g; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.g IS '日期时间';


--
-- Name: COLUMN gen_demo.h; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.h IS '长文本';


--
-- Name: COLUMN gen_demo.i; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.i IS '元数据(JSON格式)';


--
-- Name: COLUMN gen_demo.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.id IS '主键ID';


--
-- Name: COLUMN gen_demo.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_demo.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN gen_demo.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.description IS '备注/描述';


--
-- Name: COLUMN gen_demo.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.created_time IS '创建时间';


--
-- Name: COLUMN gen_demo.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.updated_time IS '更新时间';


--
-- Name: COLUMN gen_demo.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.created_id IS '创建人ID';


--
-- Name: COLUMN gen_demo.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo.updated_id IS '更新人ID';


--
-- Name: gen_demo01; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.gen_demo01 (
    name character varying(64) NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.gen_demo01 OWNER TO root;

--
-- Name: TABLE gen_demo01; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.gen_demo01 IS '示例1表';


--
-- Name: COLUMN gen_demo01.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo01.name IS '名称';


--
-- Name: COLUMN gen_demo01.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo01.id IS '主键ID';


--
-- Name: COLUMN gen_demo01.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo01.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_demo01.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo01.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN gen_demo01.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo01.description IS '备注/描述';


--
-- Name: COLUMN gen_demo01.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo01.created_time IS '创建时间';


--
-- Name: COLUMN gen_demo01.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo01.updated_time IS '更新时间';


--
-- Name: COLUMN gen_demo01.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo01.created_id IS '创建人ID';


--
-- Name: COLUMN gen_demo01.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_demo01.updated_id IS '更新人ID';


--
-- Name: gen_demo01_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.gen_demo01_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_demo01_id_seq OWNER TO root;

--
-- Name: gen_demo01_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.gen_demo01_id_seq OWNED BY public.gen_demo01.id;


--
-- Name: gen_demo_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.gen_demo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_demo_id_seq OWNER TO root;

--
-- Name: gen_demo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.gen_demo_id_seq OWNED BY public.gen_demo.id;


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
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
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
-- Name: COLUMN gen_table.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.id IS '主键ID';


--
-- Name: COLUMN gen_table.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_table.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN gen_table.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.description IS '备注/描述';


--
-- Name: COLUMN gen_table.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.created_time IS '创建时间';


--
-- Name: COLUMN gen_table.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.updated_time IS '更新时间';


--
-- Name: COLUMN gen_table.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.created_id IS '创建人ID';


--
-- Name: COLUMN gen_table.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table.updated_id IS '更新人ID';


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
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
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

COMMENT ON COLUMN public.gen_table_column.html_type IS '显示类型';


--
-- Name: COLUMN gen_table_column.dict_type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.dict_type IS '字典类型';


--
-- Name: COLUMN gen_table_column.sort; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.sort IS '排序';


--
-- Name: COLUMN gen_table_column.table_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.table_id IS '归属表编号';


--
-- Name: COLUMN gen_table_column.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.id IS '主键ID';


--
-- Name: COLUMN gen_table_column.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_table_column.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN gen_table_column.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.description IS '备注/描述';


--
-- Name: COLUMN gen_table_column.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.created_time IS '创建时间';


--
-- Name: COLUMN gen_table_column.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.updated_time IS '更新时间';


--
-- Name: COLUMN gen_table_column.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.created_id IS '创建人ID';


--
-- Name: COLUMN gen_table_column.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.gen_table_column.updated_id IS '更新人ID';


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
-- Name: sys_dept; Type: TABLE; Schema: public; Owner: root
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
-- Name: COLUMN sys_dept.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_dept.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.description IS '备注/描述';


--
-- Name: COLUMN sys_dept.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.created_time IS '创建时间';


--
-- Name: COLUMN sys_dept.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dept.updated_time IS '更新时间';


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


ALTER TABLE public.sys_dict_data OWNER TO root;

--
-- Name: TABLE sys_dict_data; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_dict_data IS '字典数据表';


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

COMMENT ON COLUMN public.sys_dict_data.is_default IS '是否默认（True是 False否）';


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
-- Name: COLUMN sys_dict_data.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_dict_data.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.description IS '备注/描述';


--
-- Name: COLUMN sys_dict_data.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.created_time IS '创建时间';


--
-- Name: COLUMN sys_dict_data.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_data.updated_time IS '更新时间';


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
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
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
-- Name: COLUMN sys_dict_type.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.id IS '主键ID';


--
-- Name: COLUMN sys_dict_type.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_dict_type.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_dict_type.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.description IS '备注/描述';


--
-- Name: COLUMN sys_dict_type.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.created_time IS '创建时间';


--
-- Name: COLUMN sys_dict_type.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_dict_type.updated_time IS '更新时间';


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
-- Name: sys_log; Type: TABLE; Schema: public; Owner: root
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


ALTER TABLE public.sys_log OWNER TO root;

--
-- Name: TABLE sys_log; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_log IS '系统日志表';


--
-- Name: COLUMN sys_log.type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.type IS '日志类型(1登录日志 2操作日志)';


--
-- Name: COLUMN sys_log.request_path; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.request_path IS '请求路径';


--
-- Name: COLUMN sys_log.request_method; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.request_method IS '请求方式';


--
-- Name: COLUMN sys_log.request_payload; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.request_payload IS '请求体';


--
-- Name: COLUMN sys_log.request_ip; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.request_ip IS '请求IP地址';


--
-- Name: COLUMN sys_log.login_location; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.login_location IS '登录位置';


--
-- Name: COLUMN sys_log.request_os; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.request_os IS '操作系统';


--
-- Name: COLUMN sys_log.request_browser; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.request_browser IS '浏览器';


--
-- Name: COLUMN sys_log.response_code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.response_code IS '响应状态码';


--
-- Name: COLUMN sys_log.response_json; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.response_json IS '响应体';


--
-- Name: COLUMN sys_log.process_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.process_time IS '处理时间';


--
-- Name: COLUMN sys_log.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.id IS '主键ID';


--
-- Name: COLUMN sys_log.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_log.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_log.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.description IS '备注/描述';


--
-- Name: COLUMN sys_log.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.created_time IS '创建时间';


--
-- Name: COLUMN sys_log.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.updated_time IS '更新时间';


--
-- Name: COLUMN sys_log.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.created_id IS '创建人ID';


--
-- Name: COLUMN sys_log.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_log.updated_id IS '更新人ID';


--
-- Name: sys_log_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_log_id_seq OWNER TO root;

--
-- Name: sys_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_log_id_seq OWNED BY public.sys_log.id;


--
-- Name: sys_menu; Type: TABLE; Schema: public; Owner: root
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


ALTER TABLE public.sys_menu OWNER TO root;

--
-- Name: TABLE sys_menu; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_menu IS '菜单表';


--
-- Name: COLUMN sys_menu.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.name IS '菜单名称';


--
-- Name: COLUMN sys_menu.type; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.type IS '菜单类型(1:目录 2:菜单 3:按钮/权限 4:链接)';


--
-- Name: COLUMN sys_menu."order"; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu."order" IS '显示排序';


--
-- Name: COLUMN sys_menu.permission; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.permission IS '权限标识(如:module_system:user:query)';


--
-- Name: COLUMN sys_menu.icon; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.icon IS '菜单图标';


--
-- Name: COLUMN sys_menu.route_name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.route_name IS '路由名称';


--
-- Name: COLUMN sys_menu.route_path; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.route_path IS '路由路径';


--
-- Name: COLUMN sys_menu.component_path; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.component_path IS '组件路径';


--
-- Name: COLUMN sys_menu.redirect; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.redirect IS '重定向地址';


--
-- Name: COLUMN sys_menu.hidden; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.hidden IS '是否隐藏(True:隐藏 False:显示)';


--
-- Name: COLUMN sys_menu.keep_alive; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.keep_alive IS '是否缓存(True:是 False:否)';


--
-- Name: COLUMN sys_menu.always_show; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.always_show IS '是否始终显示(True:是 False:否)';


--
-- Name: COLUMN sys_menu.title; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.title IS '菜单标题';


--
-- Name: COLUMN sys_menu.params; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.params IS '路由参数(JSON对象)';


--
-- Name: COLUMN sys_menu.affix; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.affix IS '是否固定标签页(True:是 False:否)';


--
-- Name: COLUMN sys_menu.parent_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.parent_id IS '父菜单ID';


--
-- Name: COLUMN sys_menu.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.id IS '主键ID';


--
-- Name: COLUMN sys_menu.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_menu.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_menu.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.description IS '备注/描述';


--
-- Name: COLUMN sys_menu.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.created_time IS '创建时间';


--
-- Name: COLUMN sys_menu.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_menu.updated_time IS '更新时间';


--
-- Name: sys_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_menu_id_seq OWNER TO root;

--
-- Name: sys_menu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_menu_id_seq OWNED BY public.sys_menu.id;


--
-- Name: sys_notice; Type: TABLE; Schema: public; Owner: root
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
-- Name: COLUMN sys_notice.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.id IS '主键ID';


--
-- Name: COLUMN sys_notice.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_notice.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_notice.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.description IS '备注/描述';


--
-- Name: COLUMN sys_notice.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.created_time IS '创建时间';


--
-- Name: COLUMN sys_notice.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.updated_time IS '更新时间';


--
-- Name: COLUMN sys_notice.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.created_id IS '创建人ID';


--
-- Name: COLUMN sys_notice.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_notice.updated_id IS '更新人ID';


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
-- Name: sys_param; Type: TABLE; Schema: public; Owner: root
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
-- Name: COLUMN sys_param.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.id IS '主键ID';


--
-- Name: COLUMN sys_param.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_param.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_param.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.description IS '备注/描述';


--
-- Name: COLUMN sys_param.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.created_time IS '创建时间';


--
-- Name: COLUMN sys_param.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_param.updated_time IS '更新时间';


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
-- Name: COLUMN sys_position."order"; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position."order" IS '显示排序';


--
-- Name: COLUMN sys_position.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.id IS '主键ID';


--
-- Name: COLUMN sys_position.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_position.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_position.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.description IS '备注/描述';


--
-- Name: COLUMN sys_position.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.created_time IS '创建时间';


--
-- Name: COLUMN sys_position.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.updated_time IS '更新时间';


--
-- Name: COLUMN sys_position.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.created_id IS '创建人ID';


--
-- Name: COLUMN sys_position.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_position.updated_id IS '更新人ID';


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
-- Name: COLUMN sys_role.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_role.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.description IS '备注/描述';


--
-- Name: COLUMN sys_role.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.created_time IS '创建时间';


--
-- Name: COLUMN sys_role.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_role.updated_time IS '更新时间';


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
-- Name: COLUMN sys_user.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_user.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.description IS '备注/描述';


--
-- Name: COLUMN sys_user.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.created_time IS '创建时间';


--
-- Name: COLUMN sys_user.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.updated_time IS '更新时间';


--
-- Name: COLUMN sys_user.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.created_id IS '创建人ID';


--
-- Name: COLUMN sys_user.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_user.updated_id IS '更新人ID';


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
-- Name: COLUMN task_job.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.status IS '执行状态';


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
-- Name: COLUMN task_job.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.id IS '主键ID';


--
-- Name: COLUMN task_job.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_job.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.description IS '备注/描述';


--
-- Name: COLUMN task_job.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.created_time IS '创建时间';


--
-- Name: COLUMN task_job.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_job.updated_time IS '更新时间';


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
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
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
-- Name: COLUMN task_node.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.id IS '主键ID';


--
-- Name: COLUMN task_node.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_node.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN task_node.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.description IS '备注/描述';


--
-- Name: COLUMN task_node.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.created_time IS '创建时间';


--
-- Name: COLUMN task_node.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.updated_time IS '更新时间';


--
-- Name: COLUMN task_node.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.created_id IS '创建人ID';


--
-- Name: COLUMN task_node.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_node.updated_id IS '更新人ID';


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
    workflow_status character varying(32) NOT NULL,
    nodes json,
    edges json,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
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
-- Name: COLUMN task_workflow.workflow_status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.workflow_status IS '流程状态: draft/published/archived';


--
-- Name: COLUMN task_workflow.nodes; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.nodes IS 'Vue Flow nodes JSON';


--
-- Name: COLUMN task_workflow.edges; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.edges IS 'Vue Flow edges JSON';


--
-- Name: COLUMN task_workflow.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.id IS '主键ID';


--
-- Name: COLUMN task_workflow.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_workflow.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN task_workflow.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.description IS '备注/描述';


--
-- Name: COLUMN task_workflow.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.created_time IS '创建时间';


--
-- Name: COLUMN task_workflow.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.updated_time IS '更新时间';


--
-- Name: COLUMN task_workflow.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.created_id IS '创建人ID';


--
-- Name: COLUMN task_workflow.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow.updated_id IS '更新人ID';


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
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
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
-- Name: COLUMN task_workflow_node_type.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.id IS '主键ID';


--
-- Name: COLUMN task_workflow_node_type.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN task_workflow_node_type.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN task_workflow_node_type.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.description IS '备注/描述';


--
-- Name: COLUMN task_workflow_node_type.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.created_time IS '创建时间';


--
-- Name: COLUMN task_workflow_node_type.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.updated_time IS '更新时间';


--
-- Name: COLUMN task_workflow_node_type.created_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.created_id IS '创建人ID';


--
-- Name: COLUMN task_workflow_node_type.updated_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.task_workflow_node_type.updated_id IS '更新人ID';


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
-- Name: app_portal id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.app_portal ALTER COLUMN id SET DEFAULT nextval('public.app_portal_id_seq'::regclass);


--
-- Name: gen_demo id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_demo ALTER COLUMN id SET DEFAULT nextval('public.gen_demo_id_seq'::regclass);


--
-- Name: gen_demo01 id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_demo01 ALTER COLUMN id SET DEFAULT nextval('public.gen_demo01_id_seq'::regclass);


--
-- Name: gen_table id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table ALTER COLUMN id SET DEFAULT nextval('public.gen_table_id_seq'::regclass);


--
-- Name: gen_table_column id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table_column ALTER COLUMN id SET DEFAULT nextval('public.gen_table_column_id_seq'::regclass);


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
-- Name: sys_log id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_log ALTER COLUMN id SET DEFAULT nextval('public.sys_log_id_seq'::regclass);


--
-- Name: sys_menu id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_menu ALTER COLUMN id SET DEFAULT nextval('public.sys_menu_id_seq'::regclass);


--
-- Name: sys_notice id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice ALTER COLUMN id SET DEFAULT nextval('public.sys_notice_id_seq'::regclass);


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
-- Data for Name: agno_schema_versions; Type: TABLE DATA; Schema: ai; Owner: root
--

COPY ai.agno_schema_versions (table_name, version, created_at, updated_at) FROM stdin;
agno_sessions	2.5.0	2026-03-10T22:38:46.429268	2026-03-10T22:38:46.429268
\.


--
-- Data for Name: agno_sessions; Type: TABLE DATA; Schema: ai; Owner: root
--

COPY ai.agno_sessions (session_id, session_type, agent_id, team_id, workflow_id, user_id, session_data, agent_data, team_data, workflow_data, metadata, runs, summary, created_at, updated_at) FROM stdin;
d0375348-cc9c-4103-a7ce-18d14560a785	team	\N	1	\N	admin	{"session_name": "新对话", "session_state": {}, "session_metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 898, "total_tokens": 915, "output_tokens": 17, "cache_read_tokens": 320}]}, "input_tokens": 898, "total_tokens": 915, "output_tokens": 17, "cache_read_tokens": 320}}	\N	null	\N	null	[{"input": {"input_content": "你好"}, "model": "deepseek-chat", "tools": [], "run_id": "44f0df2a-aaff-403f-bbb7-de1081d45580", "status": "COMPLETED", "content": "你好！我是你的AI助手，很高兴为你服务。有什么我可以帮助你的吗？", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 898, "total_tokens": 915, "output_tokens": 17, "cache_read_tokens": 320}]}, "duration": 2.4872381659988605, "input_tokens": 898, "total_tokens": 915, "output_tokens": 17, "cache_read_tokens": 320, "time_to_first_token": 2.4092763329990703}, "team_id": "1", "user_id": "admin", "messages": [{"id": "6f9ce5a8-ac26-4ca3-ada9-459641e0225c", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-12 23:50:27.983400.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1773330627, "from_history": false, "stop_after_tool_call": false}, {"id": "9ee3931d-2f8f-439a-8495-28c407e1676a", "role": "user", "content": "你好", "created_at": 1773330627, "from_history": false, "stop_after_tool_call": false}, {"id": "900ca747-7b34-44f4-ae74-e6570804fcd0", "role": "assistant", "content": "你好！我是你的AI助手，很高兴为你服务。有什么我可以帮助你的吗？", "metrics": {"duration": 2.3864872499998455, "input_tokens": 898, "total_tokens": 915, "output_tokens": 17, "cache_read_tokens": 320, "time_to_first_token": 2.3864872499998455}, "created_at": 1773330627, "from_history": false, "provider_data": {"id": "ee4835e4-1a1e-4c33-b079-ec99ae7a1b55", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}, "stop_after_tool_call": false}], "created_at": 1773330627, "session_id": "d0375348-cc9c-4103-a7ce-18d14560a785", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "ee4835e4-1a1e-4c33-b079-ec99ae7a1b55", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}}]	null	1773330627	1773330630
70f63e6b-f073-4486-8b17-a98cb4a5f4fa	team	\N	1	\N	admin	{"session_name": "在吗", "session_state": {}, "session_metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 1811, "total_tokens": 1842, "output_tokens": 31, "cache_read_tokens": 640}]}, "input_tokens": 1811, "total_tokens": 1842, "output_tokens": 31, "cache_read_tokens": 640}}	\N	null	\N	null	[{"input": {"input_content": "在吗"}, "model": "deepseek-chat", "events": [], "run_id": "bffc5320-8369-471d-814b-ca66a474f358", "status": "COMPLETED", "content": "我在的！有什么可以帮助您的吗？", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 899, "total_tokens": 907, "output_tokens": 8, "cache_read_tokens": 320}]}, "duration": 2.5330075420006324, "input_tokens": 899, "total_tokens": 907, "output_tokens": 8, "cache_read_tokens": 320, "time_to_first_token": 1.714065957999992}, "team_id": "1", "user_id": "admin", "messages": [{"id": "7a9e0dfd-3750-4dac-913f-bb07ad2e7b20", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-12 23:26:49.742737.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1773329209, "from_history": false, "stop_after_tool_call": false}, {"id": "04fdabb1-9f2c-4e9b-b133-b834a3d05ab8", "role": "user", "content": "在吗", "created_at": 1773329209, "from_history": false, "stop_after_tool_call": false}, {"id": "711208f2-81e3-4cd6-94a5-042e75f6cf08", "role": "assistant", "content": "我在的！有什么可以帮助您的吗？", "metrics": {"input_tokens": 899, "total_tokens": 907, "output_tokens": 8, "cache_read_tokens": 320, "time_to_first_token": 1.6393582500004413}, "created_at": 1773329209, "from_history": false, "provider_data": {"id": "8f1c6ef1-d4f3-413b-ba35-575a5f02bcde", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}, "stop_after_tool_call": false}], "created_at": 1773329209, "session_id": "70f63e6b-f073-4486-8b17-a98cb4a5f4fa", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "8f1c6ef1-d4f3-413b-ba35-575a5f02bcde", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}}, {"input": {"input_content": "你是谁"}, "model": "deepseek-chat", "run_id": "2636867a-f6e4-4eca-b201-68f5d0a12ffa", "status": "COMPLETED", "content": "我是您的AI助手，可以帮助您回答问题、提供信息或协助处理各种任务。有什么需要我帮忙的吗？", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 912, "total_tokens": 935, "output_tokens": 23, "cache_read_tokens": 320}]}, "duration": 3.5702720829995087, "input_tokens": 912, "total_tokens": 935, "output_tokens": 23, "cache_read_tokens": 320, "time_to_first_token": 1.6412430000000313}, "team_id": "1", "user_id": "admin", "messages": [{"id": "0c9fc707-6fec-4487-8475-838a7ee9e31b", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-13 00:19:14.591494.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1773332354, "from_history": false, "stop_after_tool_call": false}, {"id": "f6c48ec9-213b-4e73-a056-c241b5b9a88e", "role": "user", "content": "你是谁", "created_at": 1773332354, "from_history": false, "stop_after_tool_call": false}, {"id": "c4b61a03-4789-4227-81a6-0ce10c32251b", "role": "assistant", "content": "我是您的AI助手，可以帮助您回答问题、提供信息或协助处理各种任务。有什么需要我帮忙的吗？", "metrics": {"input_tokens": 912, "total_tokens": 935, "output_tokens": 23, "cache_read_tokens": 320, "time_to_first_token": 1.5480335829997784}, "created_at": 1773332354, "from_history": false, "provider_data": {"id": "988b5a84-e099-44a0-99c8-9f5eff841b7a", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}, "stop_after_tool_call": false}], "created_at": 1773332354, "session_id": "70f63e6b-f073-4486-8b17-a98cb4a5f4fa", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "988b5a84-e099-44a0-99c8-9f5eff841b7a", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}}]	null	1773329209	1773332358
8e21f309-8b73-45b9-966a-37220a628620	team	\N	1	\N	admin	{"session_name": "你是谁", "session_state": {}, "session_metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 898, "total_tokens": 931, "output_tokens": 33, "cache_read_tokens": 320}]}, "input_tokens": 898, "total_tokens": 931, "output_tokens": 33, "cache_read_tokens": 320}}	\N	null	\N	null	[{"input": {"input_content": "你是谁"}, "model": "deepseek-chat", "run_id": "973da0dc-6842-4030-bf31-dba0bf305fb8", "status": "COMPLETED", "content": "我是您的AI助手，可以帮助您回答问题和提供帮助。我可以协调一个专门团队来处理各种任务，也可以直接回答简单的问题。\\n\\n有什么我可以为您做的吗？", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 898, "total_tokens": 931, "output_tokens": 33, "cache_read_tokens": 320}]}, "duration": 3.7604397920003976, "input_tokens": 898, "total_tokens": 931, "output_tokens": 33, "cache_read_tokens": 320, "time_to_first_token": 1.9425657499996305}, "team_id": "1", "user_id": "admin", "messages": [{"id": "380b9750-36aa-4af2-a44a-457f9c0ed717", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-12 23:42:23.352241.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1773330143, "from_history": false, "stop_after_tool_call": false}, {"id": "b159f3aa-a036-44c2-b1d6-e6bfe44acbef", "role": "user", "content": "你是谁", "created_at": 1773330143, "from_history": false, "stop_after_tool_call": false}, {"id": "692d4bf2-aaae-4fa1-85cd-8a87fae2e7ac", "role": "assistant", "content": "我是您的AI助手，可以帮助您回答问题和提供帮助。我可以协调一个专门团队来处理各种任务，也可以直接回答简单的问题。\\n\\n有什么我可以为您做的吗？", "metrics": {"input_tokens": 898, "total_tokens": 931, "output_tokens": 33, "cache_read_tokens": 320, "time_to_first_token": 1.8599242089985637}, "created_at": 1773330143, "from_history": false, "provider_data": {"id": "f0a17d67-7f1e-48de-b34b-96a3dec94f4c", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}, "stop_after_tool_call": false}], "created_at": 1773330143, "session_id": "8e21f309-8b73-45b9-966a-37220a628620", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "f0a17d67-7f1e-48de-b34b-96a3dec94f4c", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}}]	null	1773330143	1773330147
93c0388f-8227-430a-8408-3369b89b0f99	team	\N	1	\N	admin	{"session_name": "你好他", "session_state": {}, "session_metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 899, "total_tokens": 915, "output_tokens": 16}]}, "input_tokens": 899, "total_tokens": 915, "output_tokens": 16}}	\N	null	\N	null	[{"input": {"input_content": "你好他"}, "model": "deepseek-chat", "run_id": "ea68973a-637a-42c3-b4da-7713c21f7b72", "status": "COMPLETED", "content": "你好！我是AI助手，很高兴为您服务。有什么我可以帮助您的吗？", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 899, "total_tokens": 915, "output_tokens": 16}]}, "duration": 2.8043415420033853, "input_tokens": 899, "total_tokens": 915, "output_tokens": 16, "time_to_first_token": 1.8211426670022774}, "team_id": "1", "user_id": "admin", "messages": [{"id": "a1b9e77c-9d9e-4973-a0cf-fab8aa0150b1", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-29 20:38:25.231562.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1774787905, "from_history": false, "stop_after_tool_call": false}, {"id": "456f3a81-3084-49fc-877d-afbe04ffb9b7", "role": "user", "content": "你好他", "created_at": 1774787905, "from_history": false, "stop_after_tool_call": false}, {"id": "7747c421-a7d0-4db8-991e-f69267bdc7c5", "role": "assistant", "content": "你好！我是AI助手，很高兴为您服务。有什么我可以帮助您的吗？", "metrics": {"input_tokens": 899, "total_tokens": 915, "output_tokens": 16, "time_to_first_token": 1.7007297909985937}, "created_at": 1774787905, "from_history": false, "provider_data": {"id": "666d6f63-0b0e-49b0-8df0-6ab39d9039fc", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache_new_kvcache"}, "stop_after_tool_call": false}], "created_at": 1774787905, "session_id": "93c0388f-8227-430a-8408-3369b89b0f99", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "666d6f63-0b0e-49b0-8df0-6ab39d9039fc", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache_new_kvcache"}}]	null	1774787904	1774787907
0e2076c7-0c72-45c0-a97b-c170413720e9	team	\N	1	\N	admin	{"session_name": "你是男的女的", "session_state": {}, "session_metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 5926, "total_tokens": 6293, "output_tokens": 367, "cache_read_tokens": 1600}]}, "input_tokens": 5926, "total_tokens": 6293, "output_tokens": 367, "cache_read_tokens": 1600}}	\N	null	\N	null	[{"input": {"input_content": "你是男的女的"}, "model": "deepseek-chat", "events": [], "run_id": "99a1fea8-2950-4f2b-a2f4-63212f52c5fb", "status": "COMPLETED", "content": "我是一个AI助手，没有性别之分。我是由代码和算法构成的数字实体，旨在为您提供帮助和回答问题。\\n\\n如果您有其他问题或需要帮助，请随时告诉我！", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 901, "total_tokens": 936, "output_tokens": 35, "cache_read_tokens": 320}]}, "duration": 3.824642333000156, "input_tokens": 901, "total_tokens": 936, "output_tokens": 35, "cache_read_tokens": 320, "time_to_first_token": 1.7806427080013236}, "team_id": "1", "user_id": "admin", "messages": [{"id": "8539d5ee-a817-4710-822d-99686642c4df", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-13 00:09:08.236156.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1773331748, "from_history": false, "stop_after_tool_call": false}, {"id": "18ed9cf5-a2a5-421e-bbb9-946f621d2a2a", "role": "user", "content": "你是男的女的", "created_at": 1773331748, "from_history": false, "stop_after_tool_call": false}, {"id": "7b3a3aa1-1fb8-4f1a-8a2c-298fef38cd7e", "role": "assistant", "content": "我是一个AI助手，没有性别之分。我是由代码和算法构成的数字实体，旨在为您提供帮助和回答问题。\\n\\n如果您有其他问题或需要帮助，请随时告诉我！", "metrics": {"input_tokens": 901, "total_tokens": 936, "output_tokens": 35, "cache_read_tokens": 320, "time_to_first_token": 1.6999175000000832}, "created_at": 1773331748, "from_history": false, "provider_data": {"id": "a1a3e8f4-dad6-45d6-9338-8c33d060f914", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}, "stop_after_tool_call": false}], "created_at": 1773331748, "session_id": "0e2076c7-0c72-45c0-a97b-c170413720e9", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "a1a3e8f4-dad6-45d6-9338-8c33d060f914", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}}, {"input": {"input_content": "好的我知道了"}, "model": "deepseek-chat", "events": [], "run_id": "9bc121c8-78e2-44b9-9ebd-758d33e845f1", "status": "COMPLETED", "content": "好的！如果您有任何其他问题或需要帮助的地方，随时可以告诉我。我很乐意为您提供帮助！", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 942, "total_tokens": 964, "output_tokens": 22, "cache_read_tokens": 320}]}, "duration": 2.982405832999575, "input_tokens": 942, "total_tokens": 964, "output_tokens": 22, "cache_read_tokens": 320, "time_to_first_token": 1.466743332999613}, "team_id": "1", "user_id": "admin", "messages": [{"id": "854713e7-3220-44c8-8c04-97eae9e9eb03", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-13 00:11:22.906936.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1773331882, "from_history": false, "stop_after_tool_call": false}, {"id": "7f39e100-a08f-46b9-ba19-3492e7e9e6bd", "role": "user", "content": "好的我知道了", "created_at": 1773331882, "from_history": false, "stop_after_tool_call": false}, {"id": "318823e2-fb6a-48fd-9692-a5dcb407e77f", "role": "assistant", "content": "好的！如果您有任何其他问题或需要帮助的地方，随时可以告诉我。我很乐意为您提供帮助！", "metrics": {"input_tokens": 942, "total_tokens": 964, "output_tokens": 22, "cache_read_tokens": 320, "time_to_first_token": 1.3560426669992012}, "created_at": 1773331882, "from_history": false, "provider_data": {"id": "d918fcc8-da81-4463-9213-72dcf3109dd8", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}, "stop_after_tool_call": false}], "created_at": 1773331882, "session_id": "0e2076c7-0c72-45c0-a97b-c170413720e9", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "d918fcc8-da81-4463-9213-72dcf3109dd8", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}}, {"input": {"input_content": "以后我再找你"}, "model": "deepseek-chat", "events": [], "run_id": "5395a65a-f7f6-4c82-b9c3-8e4f75f11312", "status": "COMPLETED", "content": "好的，随时欢迎！我会一直在这里，当您需要帮助、有问题或者想聊天的时候，随时可以回来找我。\\n\\n祝您一切顺利！👋", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 971, "total_tokens": 1003, "output_tokens": 32, "cache_read_tokens": 320}]}, "duration": 3.5782694999998057, "input_tokens": 971, "total_tokens": 1003, "output_tokens": 32, "cache_read_tokens": 320, "time_to_first_token": 1.597690667000279}, "team_id": "1", "user_id": "admin", "messages": [{"id": "96f7f716-55d0-450d-946b-2a932e76cbd4", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-13 00:15:15.297981.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1773332115, "from_history": false, "stop_after_tool_call": false}, {"id": "a38aa282-1009-41ca-b637-5e035d3df1cd", "role": "user", "content": "以后我再找你", "created_at": 1773332115, "from_history": false, "stop_after_tool_call": false}, {"id": "bbfae894-e2d8-4ba6-bd9e-192e8a8f7dba", "role": "assistant", "content": "好的，随时欢迎！我会一直在这里，当您需要帮助、有问题或者想聊天的时候，随时可以回来找我。\\n\\n祝您一切顺利！👋", "metrics": {"input_tokens": 971, "total_tokens": 1003, "output_tokens": 32, "cache_read_tokens": 320, "time_to_first_token": 1.5115680420003628}, "created_at": 1773332115, "from_history": false, "provider_data": {"id": "bf2c9e44-0665-45e8-847f-f1b3d06bde6c", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}, "stop_after_tool_call": false}], "created_at": 1773332115, "session_id": "0e2076c7-0c72-45c0-a97b-c170413720e9", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "bf2c9e44-0665-45e8-847f-f1b3d06bde6c", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache"}}, {"input": {"input_content": "在吗"}, "model": "deepseek-chat", "events": [], "run_id": "791d08b1-3a9d-4caa-aaf1-afd7bcf55b71", "status": "COMPLETED", "content": "在的！我一直都在这里。有什么可以帮您的吗？", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 1009, "total_tokens": 1022, "output_tokens": 13}]}, "duration": 2.6353677920005794, "input_tokens": 1009, "total_tokens": 1022, "output_tokens": 13, "time_to_first_token": 1.9605698750001466}, "team_id": "1", "user_id": "admin", "messages": [{"id": "6812fc0c-06f4-4e98-b083-1bc3cceef89a", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-23 23:08:13.076824.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1774278493, "from_history": false, "stop_after_tool_call": false}, {"id": "5f7e5593-d788-44dd-a4f9-81dc8a78df2c", "role": "user", "content": "在吗", "created_at": 1774278493, "from_history": false, "stop_after_tool_call": false}, {"id": "af17b0d7-8cb7-4b78-aff0-96f9e218976e", "role": "assistant", "content": "在的！我一直都在这里。有什么可以帮您的吗？", "metrics": {"input_tokens": 1009, "total_tokens": 1022, "output_tokens": 13, "time_to_first_token": 1.8868432919998668}, "created_at": 1774278493, "from_history": false, "provider_data": {"id": "b75a5129-9af1-4849-9a6a-ca308eef0340", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache_new_kvcache"}, "stop_after_tool_call": false}], "created_at": 1774278493, "session_id": "0e2076c7-0c72-45c0-a97b-c170413720e9", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "b75a5129-9af1-4849-9a6a-ca308eef0340", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache_new_kvcache"}}, {"input": {"input_content": "帮我写一个python的hello worl"}, "model": "deepseek-chat", "events": [], "run_id": "9a7cc854-f560-46f2-86f4-0c707883b257", "status": "COMPLETED", "content": "我来帮您写一个Python的\\"Hello World\\"程序。这是一个非常简单的入门程序：\\n\\n```python\\n# 最简单的Hello World程序\\nprint(\\"Hello World\\")\\n\\n# 或者使用变量\\nmessage = \\"Hello World\\"\\nprint(message)\\n\\n# 或者使用函数\\ndef say_hello():\\n    print(\\"Hello World\\")\\n\\nsay_hello()\\n```\\n\\n**运行方法：**\\n1. 将代码保存为 `hello.py` 文件\\n2. 在命令行中运行：`python hello.py`\\n3. 或者直接在Python解释器中运行\\n\\n**输出结果：**\\n```\\nHello World\\n```\\n\\n这是学习Python编程的第一步！您想了解更复杂的Python程序吗？", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 991, "total_tokens": 1129, "output_tokens": 138, "cache_read_tokens": 320}]}, "duration": 6.201454957999886, "input_tokens": 991, "total_tokens": 1129, "output_tokens": 138, "cache_read_tokens": 320, "time_to_first_token": 1.4080830000002607}, "team_id": "1", "user_id": "admin", "messages": [{"id": "cc1002e7-82f0-45e2-b8db-160129880afe", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-23 23:08:38.810848.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1774278518, "from_history": false, "stop_after_tool_call": false}, {"id": "518695f7-e8fd-4ec2-a009-4b9caade1d1d", "role": "user", "content": "帮我写一个python的hello worl", "created_at": 1774278518, "from_history": false, "stop_after_tool_call": false}, {"id": "f140147a-c0c2-44c9-8724-5809db717a55", "role": "assistant", "content": "我来帮您写一个Python的\\"Hello World\\"程序。这是一个非常简单的入门程序：\\n\\n```python\\n# 最简单的Hello World程序\\nprint(\\"Hello World\\")\\n\\n# 或者使用变量\\nmessage = \\"Hello World\\"\\nprint(message)\\n\\n# 或者使用函数\\ndef say_hello():\\n    print(\\"Hello World\\")\\n\\nsay_hello()\\n```\\n\\n**运行方法：**\\n1. 将代码保存为 `hello.py` 文件\\n2. 在命令行中运行：`python hello.py`\\n3. 或者直接在Python解释器中运行\\n\\n**输出结果：**\\n```\\nHello World\\n```\\n\\n这是学习Python编程的第一步！您想了解更复杂的Python程序吗？", "metrics": {"input_tokens": 991, "total_tokens": 1129, "output_tokens": 138, "cache_read_tokens": 320, "time_to_first_token": 1.3087896659999387}, "created_at": 1774278518, "from_history": false, "provider_data": {"id": "5b31910d-6a8e-4ba0-a2f9-dfa6f9317c30", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache_new_kvcache"}, "stop_after_tool_call": false}], "created_at": 1774278518, "session_id": "0e2076c7-0c72-45c0-a97b-c170413720e9", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "5b31910d-6a8e-4ba0-a2f9-dfa6f9317c30", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache_new_kvcache"}}, {"input": {"input_content": "请查看我提供的文件内容是什么"}, "model": "deepseek-chat", "run_id": "965fb607-566b-48c0-b4fe-87c10f3874cc", "status": "COMPLETED", "content": "我需要查看您提供的文件内容，但是目前我无法直接访问您本地的文件系统。您可以通过以下几种方式让我帮助您：\\n\\n1. **直接粘贴文件内容**：您可以将文件内容复制粘贴到聊天中\\n2. **描述文件内容**：告诉我文件的大致内容或您想了解什么\\n3. **使用代码片段**：如果是代码文件，可以用代码块格式分享\\n\\n如果您能提供文件内容，我可以帮您：\\n- 分析代码逻辑\\n- 检查语法错误\\n- 解释功能作用\\n- 提供改进建议\\n\\n请分享您想让我查看的文件内容吧！", "metrics": {"details": {"model": [{"id": "deepseek-chat", "provider": "OpenAI", "input_tokens": 1112, "total_tokens": 1239, "output_tokens": 127, "cache_read_tokens": 320}]}, "duration": 5.575905083001999, "input_tokens": 1112, "total_tokens": 1239, "output_tokens": 127, "cache_read_tokens": 320, "time_to_first_token": 1.555008583000017}, "team_id": "1", "user_id": "admin", "messages": [{"id": "87cdc130-8065-47ff-9ece-daab68c73dd7", "role": "system", "content": "You coordinate a team of specialized AI agents to fulfill the user's request. Delegate to members when their expertise or tools are needed. For straightforward requests you can handle directly — including using your own tools — respond without delegating.\\n\\n<team_members>\\n<member id=\\"admin\\" name=\\"fastapiadmin_agent\\">\\n  Role: You are a helpful AI assistant\\n  Description: 你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。\\n</member>\\n</team_members>\\n\\n<how_to_respond>\\nYou operate in coordinate mode. For requests that need member expertise, select the best member(s), delegate with clear task descriptions, and synthesize their outputs into a unified response. For requests you can handle directly — simple questions, using your own tools, or general conversation — respond without delegating.\\n\\nDelegation:\\n- Match each sub-task to the member whose role and tools are the best fit. Delegate to multiple members when the request spans different areas of expertise.\\n- Write task descriptions that are self-contained: state the goal, provide relevant context from the conversation, and describe what a good result looks like.\\n- Use only the member's ID when delegating — do not prefix it with the team ID.\\n\\nAfter receiving member responses:\\n- If a response is incomplete or off-target, re-delegate with clearer instructions or try a different member.\\n- Synthesize all results into a single coherent response. Resolve contradictions, fill gaps with your own reasoning, and add structure — do not simply concatenate member outputs.\\n</how_to_respond>\\n\\n- 保持回答简洁明了\\n- 如果不确定，请说明\\n<additional_information>\\n- Use markdown to format your answers.\\n- The current time is 2026-03-29 20:40:16.570209.\\n</additional_information>\\n\\n<expected_output>\\n中文回答\\n</expected_output>", "created_at": 1774788016, "from_history": false, "stop_after_tool_call": false}, {"id": "b7423fe7-705e-49a3-bf8c-3b406d4b044b", "role": "user", "content": "请查看我提供的文件内容是什么", "created_at": 1774788016, "from_history": false, "stop_after_tool_call": false}, {"id": "96d8afe6-bdb2-482a-a954-691c4800a591", "role": "assistant", "content": "我需要查看您提供的文件内容，但是目前我无法直接访问您本地的文件系统。您可以通过以下几种方式让我帮助您：\\n\\n1. **直接粘贴文件内容**：您可以将文件内容复制粘贴到聊天中\\n2. **描述文件内容**：告诉我文件的大致内容或您想了解什么\\n3. **使用代码片段**：如果是代码文件，可以用代码块格式分享\\n\\n如果您能提供文件内容，我可以帮您：\\n- 分析代码逻辑\\n- 检查语法错误\\n- 解释功能作用\\n- 提供改进建议\\n\\n请分享您想让我查看的文件内容吧！", "metrics": {"input_tokens": 1112, "total_tokens": 1239, "output_tokens": 127, "cache_read_tokens": 320, "time_to_first_token": 1.4296587080025347}, "created_at": 1774788016, "from_history": false, "provider_data": {"id": "26dcc6a5-7ee7-44d3-8543-69328f8bb61f", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache_new_kvcache"}, "stop_after_tool_call": false}], "created_at": 1774788016, "session_id": "0e2076c7-0c72-45c0-a97b-c170413720e9", "content_type": "str", "model_provider": "OpenAI", "member_responses": [], "model_provider_data": {"id": "26dcc6a5-7ee7-44d3-8543-69328f8bb61f", "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache_new_kvcache"}}]	null	1773331748	1774788022
\.


--
-- Data for Name: app_portal; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.app_portal (name, access_url, icon_url, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: apscheduler_jobs; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.apscheduler_jobs (id, next_run_time, job_state) FROM stdin;
\.


--
-- Data for Name: gen_demo; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.gen_demo (name, a, b, c, d, e, f, g, h, i, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: gen_demo01; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.gen_demo01 (name, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: gen_table; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.gen_table (table_name, table_comment, class_name, package_name, module_name, business_name, function_name, sub_table_name, sub_table_fk_name, parent_menu_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: gen_table_column; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.gen_table_column (column_name, column_comment, column_type, column_length, column_default, is_pk, is_increment, is_nullable, is_unique, python_type, python_field, is_insert, is_edit, is_list, is_query, query_type, html_type, dict_type, sort, table_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_dept; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_dept (name, "order", code, leader, phone, email, parent_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
集团总公司	1	GROUP	部门负责人	1582112620	deptadmin@example.com	\N	1	4ce37ab1-0966-4ab9-9315-37198a772b40	0	集团总公司	2026-04-03 00:38:22.844742	2026-04-03 00:38:22.844743
\.


--
-- Data for Name: sys_dict_data; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_dict_data (dict_sort, dict_label, dict_value, css_class, list_class, is_default, dict_type, dict_type_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
1	男	0	blue	\N	t	sys_user_sex	1	1	2de65287-0314-49ed-86ad-e523a1a05873	0	性别男	2026-04-03 00:38:22.855541	2026-04-03 00:38:22.855543
2	女	1	pink	\N	f	sys_user_sex	1	2	8a9eb506-71a8-48b3-9d3d-5106afdb0fd6	0	性别女	2026-04-03 00:38:22.855546	2026-04-03 00:38:22.855547
3	未知	2	red	\N	f	sys_user_sex	1	3	90805910-fffb-4127-8abf-64df995af724	0	性别未知	2026-04-03 00:38:22.85555	2026-04-03 00:38:22.85555
1	是	1		primary	t	sys_yes_no	2	4	c8d485c8-bcf9-46f1-9782-f16b30f10132	0	是	2026-04-03 00:38:22.855553	2026-04-03 00:38:22.855553
2	否	0		danger	f	sys_yes_no	2	5	d6999f37-270a-46d4-9a55-28c1e832f7d9	0	否	2026-04-03 00:38:22.855556	2026-04-03 00:38:22.855556
1	启用	1		primary	f	sys_common_status	3	6	0a9d64dd-a6e9-4557-89f6-8ea17d59c273	0	启用状态	2026-04-03 00:38:22.855559	2026-04-03 00:38:22.85556
2	停用	0		danger	f	sys_common_status	3	7	25981366-37b1-4104-8783-46bbc6026cf7	0	停用状态	2026-04-03 00:38:22.855562	2026-04-03 00:38:22.855563
1	通知	1	blue	warning	t	sys_notice_type	4	8	8ae2906d-a0fb-445b-95af-bb54325f6bf1	0	通知	2026-04-03 00:38:22.855565	2026-04-03 00:38:22.855566
2	公告	2	orange	success	f	sys_notice_type	4	9	07351d5a-2b16-482e-8765-673a6a853ab6	0	公告	2026-04-03 00:38:22.855568	2026-04-03 00:38:22.855569
99	其他	0		info	f	sys_oper_type	5	10	78919d05-b288-473f-81bd-4931eeba7eba	0	其他操作	2026-04-03 00:38:22.855571	2026-04-03 00:38:22.855572
1	新增	1		info	f	sys_oper_type	5	11	33dcba92-179c-481d-811d-f0c13b1b4843	0	新增操作	2026-04-03 00:38:22.855574	2026-04-03 00:38:22.855575
2	修改	2		info	f	sys_oper_type	5	12	7d41664f-3276-4d6c-93a1-cb4c42cbf2b5	0	修改操作	2026-04-03 00:38:22.855577	2026-04-03 00:38:22.855578
3	删除	3		danger	f	sys_oper_type	5	13	c220e753-e8c1-4ea2-88a8-84964538fb38	0	删除操作	2026-04-03 00:38:22.85558	2026-04-03 00:38:22.855581
4	分配权限	4		primary	f	sys_oper_type	5	14	f4b992dc-e239-4d56-9d1c-523c6a96dd5c	0	授权操作	2026-04-03 00:38:22.855583	2026-04-03 00:38:22.855584
5	导出	5		warning	f	sys_oper_type	5	15	88b94728-4c39-4377-bc44-cbe659569694	0	导出操作	2026-04-03 00:38:22.855586	2026-04-03 00:38:22.855586
6	导入	6		warning	f	sys_oper_type	5	16	0ea14b80-4b4a-4d8b-925b-65ba5106ed41	0	导入操作	2026-04-03 00:38:22.855589	2026-04-03 00:38:22.855589
7	强退	7		danger	f	sys_oper_type	5	17	06074fcf-7e02-42e3-9b8d-5d110ad7f8a1	0	强退操作	2026-04-03 00:38:22.855592	2026-04-03 00:38:22.855592
8	生成代码	8		warning	f	sys_oper_type	5	18	dcfa6d0d-e6d0-4ff7-9685-9e4c818ec41c	0	生成操作	2026-04-03 00:38:22.855595	2026-04-03 00:38:22.855595
9	清空数据	9		danger	f	sys_oper_type	5	19	9e29caba-512d-48d1-94aa-85217617daba	0	清空操作	2026-04-03 00:38:22.855598	2026-04-03 00:38:22.855598
1	默认(Memory)	default		\N	t	sys_job_store	6	20	f83f23f0-ed84-4c31-abf2-e0329fb45c3f	0	默认分组	2026-04-03 00:38:22.855601	2026-04-03 00:38:22.855601
2	数据库(Sqlalchemy)	sqlalchemy		\N	f	sys_job_store	6	21	e9b18dc9-1570-4ab7-9410-53ecdb6aec61	0	数据库分组	2026-04-03 00:38:22.855604	2026-04-03 00:38:22.855604
3	数据库(Redis)	redis		\N	f	sys_job_store	6	22	fd1a1ecd-06f6-40a3-ae9d-86d3c93a7570	0	reids分组	2026-04-03 00:38:22.855607	2026-04-03 00:38:22.855607
1	线程池	default		\N	f	sys_job_executor	7	23	90de71b4-4945-44c9-bc48-835f4c3cf5e2	0	线程池	2026-04-03 00:38:22.85561	2026-04-03 00:38:22.85561
2	进程池	processpool		\N	f	sys_job_executor	7	24	1d960b89-891e-4fba-bcd4-aa63674277b9	0	进程池	2026-04-03 00:38:22.855613	2026-04-03 00:38:22.855613
1	演示函数	scheduler_test.job		\N	t	sys_job_function	8	25	a5c9589b-3d42-4cda-975c-5a7f7c7bc7cb	0	演示函数	2026-04-03 00:38:22.855616	2026-04-03 00:38:22.855616
1	指定日期(date)	date		\N	t	sys_job_trigger	9	26	03f5463e-8ec9-4db6-992a-564d4c12fc23	0	指定日期任务触发器	2026-04-03 00:38:22.855619	2026-04-03 00:38:22.855619
2	间隔触发器(interval)	interval		\N	f	sys_job_trigger	9	27	800d8bb8-85fd-4831-a7dc-6a9d02f68a29	0	间隔触发器任务触发器	2026-04-03 00:38:22.855623	2026-04-03 00:38:22.855623
3	cron表达式	cron		\N	f	sys_job_trigger	9	28	8396804b-11d5-4b0f-b1eb-ec75070b534e	0	间隔触发器任务触发器	2026-04-03 00:38:22.855627	2026-04-03 00:38:22.855628
1	默认(default)	default		\N	t	sys_list_class	10	29	a497ec4e-5f13-4226-9c57-62b49710881c	0	默认表格回显样式	2026-04-03 00:38:22.855631	2026-04-03 00:38:22.855631
2	主要(primary)	primary		\N	f	sys_list_class	10	30	df379254-54f4-4d89-84ea-02630d1aeda1	0	主要表格回显样式	2026-04-03 00:38:22.855635	2026-04-03 00:38:22.855635
3	成功(success)	success		\N	f	sys_list_class	10	31	a3cb325b-5fa6-4022-8bab-5281447d88c1	0	成功表格回显样式	2026-04-03 00:38:22.855639	2026-04-03 00:38:22.855639
4	信息(info)	info		\N	f	sys_list_class	10	32	63c93836-b3f8-4783-a809-30a58b9b13fb	0	信息表格回显样式	2026-04-03 00:38:22.855642	2026-04-03 00:38:22.855643
5	警告(warning)	warning		\N	f	sys_list_class	10	33	5e4627ec-10d9-4108-807a-407bc5b197b7	0	警告表格回显样式	2026-04-03 00:38:22.855645	2026-04-03 00:38:22.855646
6	危险(danger)	danger		\N	f	sys_list_class	10	34	5279e91f-c5a1-4a70-b1ac-94d25bf11706	0	危险表格回显样式	2026-04-03 00:38:22.855648	2026-04-03 00:38:22.855649
\.


--
-- Data for Name: sys_dict_type; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_dict_type (dict_name, dict_type, id, uuid, status, description, created_time, updated_time) FROM stdin;
用户性别	sys_user_sex	1	80178156-0daa-41ff-8f1a-58fb3936cb4b	0	用户性别列表	2026-04-03 00:38:22.850282	2026-04-03 00:38:22.850282
系统是否	sys_yes_no	2	c2e8db3d-9514-4756-b8c9-e6d6f324d094	0	系统是否列表	2026-04-03 00:38:22.850286	2026-04-03 00:38:22.850287
系统状态	sys_common_status	3	3d7e2633-bd39-4ccb-8d0f-2dcdb503dc5d	0	系统状态	2026-04-03 00:38:22.85029	2026-04-03 00:38:22.85029
通知类型	sys_notice_type	4	7583d888-d458-48db-a44d-1a53372bb2e8	0	通知类型列表	2026-04-03 00:38:22.850293	2026-04-03 00:38:22.850293
操作类型	sys_oper_type	5	111c581d-924b-4211-ba72-d757b43d1cdc	0	操作类型列表	2026-04-03 00:38:22.850296	2026-04-03 00:38:22.850296
任务存储器	sys_job_store	6	bd889b21-f488-48ac-b326-6938ea00d287	0	任务分组列表	2026-04-03 00:38:22.850299	2026-04-03 00:38:22.8503
任务执行器	sys_job_executor	7	6ceb3045-a032-47e3-bfeb-b24ecad85ac2	0	任务执行器列表	2026-04-03 00:38:22.850302	2026-04-03 00:38:22.850303
任务函数	sys_job_function	8	aa5d6274-5692-41d3-8d58-4f15999d805f	0	任务函数列表	2026-04-03 00:38:22.850305	2026-04-03 00:38:22.850306
任务触发器	sys_job_trigger	9	4c0bdef2-afe1-4b7f-9192-004e28fb2a40	0	任务触发器列表	2026-04-03 00:38:22.850308	2026-04-03 00:38:22.850309
表格回显样式	sys_list_class	10	40bb4e53-e343-4120-8338-b0538321e44f	0	表格回显样式列表	2026-04-03 00:38:22.850312	2026-04-03 00:38:22.850312
\.


--
-- Data for Name: sys_log; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_log (type, request_path, request_method, request_payload, request_ip, login_location, request_os, request_browser, response_code, response_json, process_time, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_menu; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_menu (name, type, "order", permission, icon, route_name, route_path, component_path, redirect, hidden, keep_alive, always_show, title, params, affix, parent_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
仪表盘	1	1		client	Dashboard	/dashboard	\N	/dashboard/workplace	f	t	t	仪表盘	null	f	\N	1	62e2998b-f3c9-4005-a266-7215a6b94e44	0	初始化数据	2026-04-03 00:38:22.817306	2026-04-03 00:38:22.81731
系统管理	1	2	\N	system	System	/system	\N	/system/menu	f	t	f	系统管理	null	f	\N	2	f61df8e1-4466-4924-8121-bf69edfb0be1	0	初始化数据	2026-04-03 00:38:22.817314	2026-04-03 00:38:22.817315
监控管理	1	3	\N	monitor	Monitor	/monitor	\N	/monitor/online	f	t	f	监控管理	null	f	\N	3	4816879f-27cb-4c96-9ba9-881a15122d9e	0	初始化数据	2026-04-03 00:38:22.817318	2026-04-03 00:38:22.817319
接口管理	1	4	\N	document	Common	/common	\N	/common/docs	f	t	f	接口管理	null	f	\N	4	b37e67a0-8a3a-4a4e-a403-e4badbfd5eb9	0	初始化数据	2026-04-03 00:38:22.817322	2026-04-03 00:38:22.817322
代码管理	1	5	\N	code	Generator	/generator	\N	/generator/gencode	f	t	f	代码管理	null	f	\N	5	b36e0598-bd9c-463c-85e7-6247fa3e341a	0	代码管理	2026-04-03 00:38:22.817325	2026-04-03 00:38:22.817325
应用管理	1	6	\N	el-icon-ShoppingBag	Application	/application	\N	/application/portal	f	t	f	应用管理	null	f	\N	6	2b2a350b-0077-4a45-ab9f-c50c8bb61db0	0	初始化数据	2026-04-03 00:38:22.817328	2026-04-03 00:38:22.817329
AI管理	1	7	\N	el-icon-ChatLineSquare	AI	/ai	\N	/ai/chat	f	t	f	AI管理	null	f	\N	7	bcab7edb-1443-4aa9-82ba-f0f7d4525f02	0	AI管理	2026-04-03 00:38:22.817331	2026-04-03 00:38:22.817332
任务管理	1	8	\N	el-icon-SetUp	Task	/task	\N	/task/cronjob/job	f	t	f	任务管理	null	f	\N	8	a1d7a7de-17a6-4cf6-afaf-5e5b560d16a7	0	任务管理	2026-04-03 00:38:22.817335	2026-04-03 00:38:22.817335
案例管理	1	9	\N	menu	Example	/example	\N	/example/demo	f	t	f	案例管理	null	f	\N	9	125fc329-5fbf-4a27-91c6-388678f810af	0	案例管理	2026-04-03 00:38:22.817338	2026-04-03 00:38:22.817338
工作台	2	1	dashboard:workplace:query	el-icon-PieChart	Workplace	/dashboard/workplace	dashboard/workplace	\N	f	t	f	工作台	null	f	1	10	e30e9f48-9523-4ad0-82d4-bee5a587200b	0	初始化数据	2026-04-03 00:38:22.822468	2026-04-03 00:38:22.82247
菜单管理	2	1	module_system:menu:query	menu	Menu	/system/menu	module_system/menu/index	\N	f	t	f	菜单管理	null	f	2	11	40726a03-aa01-4a0d-a273-6a4bdd31aa58	0	初始化数据	2026-04-03 00:38:22.822473	2026-04-03 00:38:22.822474
部门管理	2	2	module_system:dept:query	tree	Dept	/system/dept	module_system/dept/index	\N	f	t	f	部门管理	null	f	2	12	aaece50f-9f79-41b6-9bf8-a8d345453df6	0	初始化数据	2026-04-03 00:38:22.822477	2026-04-03 00:38:22.822477
岗位管理	2	3	module_system:position:query	el-icon-Coordinate	Position	/system/position	module_system/position/index	\N	f	t	f	岗位管理	null	f	2	13	08cffe04-d509-4b67-80fc-69c700d6b50e	0	初始化数据	2026-04-03 00:38:22.82248	2026-04-03 00:38:22.822481
角色管理	2	4	module_system:role:query	role	Role	/system/role	module_system/role/index	\N	f	t	f	角色管理	null	f	2	14	b7a19818-5ae4-4a3e-b7e4-12392d3eb5c0	0	初始化数据	2026-04-03 00:38:22.822483	2026-04-03 00:38:22.822484
用户管理	2	5	module_system:user:query	el-icon-User	User	/system/user	module_system/user/index	\N	f	t	f	用户管理	null	f	2	15	0faee004-c5a8-4ff2-b3dc-3fb7ba59c58f	0	初始化数据	2026-04-03 00:38:22.822487	2026-04-03 00:38:22.822487
日志管理	2	6	module_system:log:query	el-icon-Aim	Log	/system/log	module_system/log/index	\N	f	t	f	日志管理	null	f	2	16	2b140cb7-9d28-4f56-843a-882fac22268b	0	初始化数据	2026-04-03 00:38:22.82249	2026-04-03 00:38:22.82249
公告管理	2	7	module_system:notice:query	bell	Notice	/system/notice	module_system/notice/index	\N	f	t	f	公告管理	null	f	2	17	744c99c7-6159-4877-a1a8-91adbf2a4c79	0	初始化数据	2026-04-03 00:38:22.822493	2026-04-03 00:38:22.822493
参数管理	2	8	module_system:param:query	setting	Params	/system/param	module_system/param/index	\N	f	t	f	参数管理	null	f	2	18	71cf75d0-9fc6-42df-ba23-2789bf2e6b78	0	初始化数据	2026-04-03 00:38:22.822496	2026-04-03 00:38:22.822496
字典管理	2	9	module_system:dict_type:query	dict	Dict	/system/dict	module_system/dict/index	\N	f	t	f	字典管理	null	f	2	19	755836fa-6aee-4a9c-81fa-786e6ff73727	0	初始化数据	2026-04-03 00:38:22.822499	2026-04-03 00:38:22.822499
在线用户	2	1	module_monitor:online:query	el-icon-Headset	MonitorOnline	/monitor/online	module_monitor/online/index	\N	f	t	f	在线用户	null	f	3	20	9475cec0-51cd-48e6-84d3-44aaddd30917	0	初始化数据	2026-04-03 00:38:22.822502	2026-04-03 00:38:22.822502
服务器监控	2	2	module_monitor:server:query	el-icon-Odometer	MonitorServer	/monitor/server	module_monitor/server/index	\N	f	t	f	服务器监控	null	f	3	21	fe5010f2-c9a4-4dbf-8ea1-1096af70f64c	0	初始化数据	2026-04-03 00:38:22.822505	2026-04-03 00:38:22.822505
缓存监控	2	3	module_monitor:cache:query	el-icon-Stopwatch	MonitorCache	/monitor/cache	module_monitor/cache/index	\N	f	t	f	缓存监控	null	f	3	22	c30e09d8-c001-4963-bb72-7032f6eb54b5	0	初始化数据	2026-04-03 00:38:22.822508	2026-04-03 00:38:22.822508
文件管理	2	4	module_monitor:resource:query	el-icon-Files	Resource	/monitor/resource	module_monitor/resource/index	\N	f	t	f	文件管理	null	f	3	23	0b4de750-79bb-4da1-826a-35b6d2acfd5c	0	初始化数据	2026-04-03 00:38:22.822511	2026-04-03 00:38:22.822511
Swagger文档	4	1	module_common:docs:query	api	Docs	/common/docs	module_common/docs/index	\N	f	t	f	Swagger文档	null	f	4	24	fe1ef1c7-bbb7-4a90-82c9-774d1d64a7ca	0	初始化数据	2026-04-03 00:38:22.822514	2026-04-03 00:38:22.822514
Redoc文档	4	2	module_common:redoc:query	el-icon-Document	Redoc	/common/redoc	module_common/redoc/index	\N	f	t	f	Redoc文档	null	f	4	25	f718f039-ec0a-4ea8-9cec-d2e1baba56d5	0	初始化数据	2026-04-03 00:38:22.822517	2026-04-03 00:38:22.822517
LangJin文档	4	3	module_common:ljdoc:query	el-icon-Document	Ljdoc	/common/ljdoc	module_common/ljdoc/index	\N	f	t	f	LangJin文档	null	f	4	26	dcc3452a-19f4-44aa-8c58-d4cd70a0cfc4	0	初始化数据	2026-04-03 00:38:22.822519	2026-04-03 00:38:22.82252
代码生成	2	1	module_generator:gencode:query	code	GenCode	/generator/gencode	module_generator/gencode/index	\N	f	t	f	代码生成	null	f	5	27	90c87bea-d474-40a2-93d1-0ea8dfcb9bd1	0	代码生成	2026-04-03 00:38:22.822522	2026-04-03 00:38:22.822523
门户应用	2	1	module_application:portal:query	el-icon-ShoppingCartFull	PortalApp	/application/portal	module_application/portal/index	\N	f	t	f	门户应用	null	f	6	28	78abae79-58d1-4cb6-ae57-9cb573e1e83f	0	初始化数据	2026-04-03 00:38:22.822526	2026-04-03 00:38:22.822526
AI智能助手	2	1	module_ai:chat:query	el-icon-ChatDotRound	Chat	/ai/chat	module_ai/chat/index	\N	f	t	f	AI智能助手	null	f	7	29	4e871c29-3555-4567-b6d5-074a8131fba8	0	AI智能助手	2026-04-03 00:38:22.82253	2026-04-03 00:38:22.822531
会话记忆	2	2	module_ai:chat:query	el-icon-ChatLineSquare	Memory	/ai/memory	module_ai/memory/index	\N	f	t	f	会话记忆	null	f	7	30	d149bad8-ff41-422a-a2d6-98ca63e2d5db	0	会话记忆管理	2026-04-03 00:38:22.822534	2026-04-03 00:38:22.822535
定时任务	1	1	\N	el-icon-Timer	Cronjob	/task/cronjob	\N	/task/cronjob/job	f	t	t	定时任务	null	f	8	31	f250cbe9-d735-4b82-adff-df24fd28a363	0	APScheduler 调度器与任务节点	2026-04-03 00:38:22.822538	2026-04-03 00:38:22.822538
工作流	1	2	\N	el-icon-SetUp	WorkflowMgr	/task/workflow-mgr	\N	/task/workflow/definition	f	t	t	工作流	null	f	8	32	65c77a59-d4e5-440e-911a-e4add7e030e9	0	流程编排与编排节点类型	2026-04-03 00:38:22.822542	2026-04-03 00:38:22.822542
示例管理	2	1	module_example:demo:query	menu	Demo	/example/demo	module_example/demo/index	\N	f	t	f	示例管理	null	f	9	33	0c69d14a-c2cc-4e3f-a513-446bf4fd090f	0	示例管理	2026-04-03 00:38:22.822545	2026-04-03 00:38:22.822546
二级目录	1	2	\N	menu	DemoDir	/example/demo-group	\N	/example/demo-group/demo01	f	t	t	二级目录	null	f	9	34	d29d145a-f1ef-40dd-ac56-1b61417731b8	0	二级目录（含三级菜单）	2026-04-03 00:38:22.822548	2026-04-03 00:38:22.822548
创建菜单	3	1	module_system:menu:create	\N	\N	\N	\N	\N	f	t	f	创建菜单	null	f	11	35	f0a0706b-bb2c-41b4-82ab-a18eab7ce5c0	0	初始化数据	2026-04-03 00:38:22.828125	2026-04-03 00:38:22.828128
修改菜单	3	2	module_system:menu:update	\N	\N	\N	\N	\N	f	t	f	修改菜单	null	f	11	36	6207280b-7247-4151-ae86-cfbae36c400f	0	初始化数据	2026-04-03 00:38:22.828133	2026-04-03 00:38:22.828133
删除菜单	3	3	module_system:menu:delete	\N	\N	\N	\N	\N	f	t	f	删除菜单	null	f	11	37	f13e4b64-6748-4406-80af-cbf4b3eb510f	0	初始化数据	2026-04-03 00:38:22.828137	2026-04-03 00:38:22.828138
批量修改菜单状态	3	4	module_system:menu:patch	\N	\N	\N	\N	\N	f	t	f	批量修改菜单状态	null	f	11	38	260530e5-c830-4f75-82fd-cb8b3090733c	0	初始化数据	2026-04-03 00:38:22.828141	2026-04-03 00:38:22.828142
详情菜单	3	5	module_system:menu:detail	\N	\N	\N	\N	\N	f	t	f	详情菜单	null	f	11	39	4fdbff8e-8492-4436-b337-d031575a4461	0	初始化数据	2026-04-03 00:38:22.828146	2026-04-03 00:38:22.828146
查询菜单	3	6	module_system:menu:query	\N	\N	\N	\N	\N	f	t	f	查询菜单	null	f	11	40	7774e438-0048-40b1-a402-9d483aa468ee	0	初始化数据	2026-04-03 00:38:22.82815	2026-04-03 00:38:22.828151
创建部门	3	1	module_system:dept:create	\N	\N	\N	\N	\N	f	t	f	创建部门	null	f	12	41	de16c4f6-3cae-4098-9d59-43cce758ac03	0	初始化数据	2026-04-03 00:38:22.828154	2026-04-03 00:38:22.828155
修改部门	3	2	module_system:dept:update	\N	\N	\N	\N	\N	f	t	f	修改部门	null	f	12	42	4917fc2d-2d92-4300-bf03-7f854f8d05b7	0	初始化数据	2026-04-03 00:38:22.828159	2026-04-03 00:38:22.828159
删除部门	3	3	module_system:dept:delete	\N	\N	\N	\N	\N	f	t	f	删除部门	null	f	12	43	63bc6057-c59b-4e7c-935b-8e723395d217	0	初始化数据	2026-04-03 00:38:22.828163	2026-04-03 00:38:22.828163
批量修改部门状态	3	4	module_system:dept:patch	\N	\N	\N	\N	\N	f	t	f	批量修改部门状态	null	f	12	44	6bf2c6c0-1298-426a-9ac4-4e7593f11843	0	初始化数据	2026-04-03 00:38:22.828167	2026-04-03 00:38:22.828167
详情部门	3	5	module_system:dept:detail	\N	\N	\N	\N	\N	f	t	f	详情部门	null	f	12	45	93555262-a17f-46d1-b49f-36edc04073f6	0	初始化数据	2026-04-03 00:38:22.828171	2026-04-03 00:38:22.828171
查询部门	3	6	module_system:dept:query	\N	\N	\N	\N	\N	f	t	f	查询部门	null	f	12	46	30146fe7-27cc-463b-8bab-47ea845957a4	0	初始化数据	2026-04-03 00:38:22.828175	2026-04-03 00:38:22.828175
创建岗位	3	1	module_system:position:create	\N	\N	\N	\N	\N	f	t	f	创建岗位	null	f	13	47	314ecbc0-b699-48c4-a226-4c03e4b96ea5	0	初始化数据	2026-04-03 00:38:22.828178	2026-04-03 00:38:22.828178
修改岗位	3	2	module_system:position:update	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	13	48	aeaa2d03-33fc-465a-ae02-d9307134584b	0	初始化数据	2026-04-03 00:38:22.828181	2026-04-03 00:38:22.828182
删除岗位	3	3	module_system:position:delete	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	13	49	b320a7b3-6b75-4db8-8f51-b2a9ea9d6110	0	初始化数据	2026-04-03 00:38:22.828186	2026-04-03 00:38:22.828187
批量修改岗位状态	3	4	module_system:position:patch	\N	\N	\N	\N	\N	f	t	f	批量修改岗位状态	null	f	13	50	e8fc484d-9560-4371-a8d0-c89f76a6454a	0	初始化数据	2026-04-03 00:38:22.82819	2026-04-03 00:38:22.828191
岗位导出	3	5	module_system:position:export	\N	\N	\N	\N	\N	f	t	f	岗位导出	null	f	13	51	30e213cc-0042-4fa0-bc06-00e40248967d	0	初始化数据	2026-04-03 00:38:22.828194	2026-04-03 00:38:22.828194
详情岗位	3	6	module_system:position:detail	\N	\N	\N	\N	\N	f	t	f	详情岗位	null	f	13	52	35f5891b-060f-4c96-9e47-3f626eac2fb6	0	初始化数据	2026-04-03 00:38:22.828197	2026-04-03 00:38:22.828197
查询岗位	3	7	module_system:position:query	\N	\N	\N	\N	\N	f	t	f	查询岗位	null	f	13	53	97059be5-b6b3-49f5-a7f6-a5f12352ed34	0	初始化数据	2026-04-03 00:38:22.8282	2026-04-03 00:38:22.8282
创建角色	3	1	module_system:role:create	\N	\N	\N	\N	\N	f	t	f	创建角色	null	f	14	54	ada3cf3b-421d-4858-801c-914fd4b59893	0	初始化数据	2026-04-03 00:38:22.828204	2026-04-03 00:38:22.828204
修改角色	3	2	module_system:role:update	\N	\N	\N	\N	\N	f	t	f	修改角色	null	f	14	55	56b2c241-9c5a-4ec1-a49c-ae8e1b3f082a	0	初始化数据	2026-04-03 00:38:22.828207	2026-04-03 00:38:22.828208
删除角色	3	3	module_system:role:delete	\N	\N	\N	\N	\N	f	t	f	删除角色	null	f	14	56	904f3ce6-d463-49b9-87cd-467c02b1379d	0	初始化数据	2026-04-03 00:38:22.828211	2026-04-03 00:38:22.828212
批量修改角色状态	3	4	module_system:role:patch	\N	\N	\N	\N	\N	f	t	f	批量修改角色状态	null	f	14	57	e0bd2c6f-634d-435d-8749-b2fc4f9a3d7a	0	初始化数据	2026-04-03 00:38:22.828215	2026-04-03 00:38:22.828216
角色导出	3	5	module_system:role:export	\N	\N	\N	\N	\N	f	t	f	角色导出	null	f	14	58	5fbc3b2d-795e-4716-99f4-0fdd57230f28	0	初始化数据	2026-04-03 00:38:22.828219	2026-04-03 00:38:22.828219
详情角色	3	6	module_system:role:detail	\N	\N	\N	\N	\N	f	t	f	详情角色	null	f	14	59	6cbe269e-7f3f-42cf-923c-d2e33ba11236	0	初始化数据	2026-04-03 00:38:22.828223	2026-04-03 00:38:22.828224
查询角色	3	7	module_system:role:query	\N	\N	\N	\N	\N	f	t	f	查询角色	null	f	14	60	0a9075d2-e7e0-4149-9bd8-42001699d825	0	初始化数据	2026-04-03 00:38:22.828228	2026-04-03 00:38:22.828228
分配权限	3	8	module_system:role:permission	\N	\N	\N	\N	\N	f	t	f	分配权限	null	f	14	61	e34e93d0-91f3-48f5-a8a8-1d1ec1971c51	0	初始化数据	2026-04-03 00:38:22.828232	2026-04-03 00:38:22.828233
创建用户	3	1	module_system:user:create	\N	\N	\N	\N	\N	f	t	f	创建用户	null	f	15	62	3029283a-317c-49dd-8096-fe324afe8fc8	0	初始化数据	2026-04-03 00:38:22.828236	2026-04-03 00:38:22.828236
修改用户	3	2	module_system:user:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	15	63	b2b5de45-2f3e-47f8-89ea-2a77e7a77ff8	0	初始化数据	2026-04-03 00:38:22.82824	2026-04-03 00:38:22.82824
删除用户	3	3	module_system:user:delete	\N	\N	\N	\N	\N	f	t	f	删除用户	null	f	15	64	1f75168d-b18b-485f-b2e4-9af404773193	0	初始化数据	2026-04-03 00:38:22.828244	2026-04-03 00:38:22.828244
批量修改用户状态	3	4	module_system:user:patch	\N	\N	\N	\N	\N	f	t	f	批量修改用户状态	null	f	15	65	11d1b540-ee61-4698-8031-6ad5fd41c44a	0	初始化数据	2026-04-03 00:38:22.828247	2026-04-03 00:38:22.828248
导出用户	3	5	module_system:user:export	\N	\N	\N	\N	\N	f	t	f	导出用户	null	f	15	66	cbcd0136-4b09-42ec-820c-3f682f38d157	0	初始化数据	2026-04-03 00:38:22.828251	2026-04-03 00:38:22.828251
导入用户	3	6	module_system:user:import	\N	\N	\N	\N	\N	f	t	f	导入用户	null	f	15	67	92a9485f-7435-4f3d-8c32-773738a74e6a	0	初始化数据	2026-04-03 00:38:22.828254	2026-04-03 00:38:22.828255
下载用户导入模板	3	7	module_system:user:download	\N	\N	\N	\N	\N	f	t	f	下载用户导入模板	null	f	15	68	88c5f60f-682a-4129-83a2-213951723505	0	初始化数据	2026-04-03 00:38:22.828258	2026-04-03 00:38:22.828259
详情用户	3	8	module_system:user:detail	\N	\N	\N	\N	\N	f	t	f	详情用户	null	f	15	69	0274f154-b8f9-4878-87d0-d552275d8a9b	0	初始化数据	2026-04-03 00:38:22.828261	2026-04-03 00:38:22.828262
查询用户	3	9	module_system:user:query	\N	\N	\N	\N	\N	f	t	f	查询用户	null	f	15	70	21ecce2c-3642-44f1-b809-bdedd9869e71	0	初始化数据	2026-04-03 00:38:22.828264	2026-04-03 00:38:22.828265
日志删除	3	1	module_system:log:delete	\N	\N	\N	\N	\N	f	t	f	日志删除	null	f	16	71	6e991841-c497-4b48-b28a-800769e3af45	0	初始化数据	2026-04-03 00:38:22.828268	2026-04-03 00:38:22.828268
日志导出	3	2	module_system:log:export	\N	\N	\N	\N	\N	f	t	f	日志导出	null	f	16	72	86f56644-0cb3-4475-94ae-79389175b583	0	初始化数据	2026-04-03 00:38:22.828271	2026-04-03 00:38:22.828271
日志详情	3	3	module_system:log:detail	\N	\N	\N	\N	\N	f	t	f	日志详情	null	f	16	73	fc1f3405-2471-4b9e-9328-00ca9bb1704a	0	初始化数据	2026-04-03 00:38:22.828273	2026-04-03 00:38:22.828274
查询日志	3	4	module_system:log:query	\N	\N	\N	\N	\N	f	t	f	查询日志	null	f	16	74	502c326c-36f7-4960-9e43-196ab3a46d78	0	初始化数据	2026-04-03 00:38:22.828276	2026-04-03 00:38:22.828277
公告创建	3	1	module_system:notice:create	\N	\N	\N	\N	\N	f	t	f	公告创建	null	f	17	75	1cf1cb16-2738-4861-a8c5-63e8075a2a3e	0	初始化数据	2026-04-03 00:38:22.828279	2026-04-03 00:38:22.82828
公告修改	3	2	module_system:notice:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	17	76	fab7eb1d-179e-4f82-a57c-05ab2c4cc8f5	0	初始化数据	2026-04-03 00:38:22.828282	2026-04-03 00:38:22.828282
公告删除	3	3	module_system:notice:delete	\N	\N	\N	\N	\N	f	t	f	公告删除	null	f	17	77	db07d84f-5d0e-4d95-ba7d-4fbb93e9b36d	0	初始化数据	2026-04-03 00:38:22.828286	2026-04-03 00:38:22.828286
公告导出	3	4	module_system:notice:export	\N	\N	\N	\N	\N	f	t	f	公告导出	null	f	17	78	d6a2fe5b-a73e-4100-a5c0-ba8e6b591db6	0	初始化数据	2026-04-03 00:38:22.828289	2026-04-03 00:38:22.828289
公告批量修改状态	3	5	module_system:notice:patch	\N	\N	\N	\N	\N	f	t	f	公告批量修改状态	null	f	17	79	dea13602-b64e-45a8-b915-fb4ef5c48823	0	初始化数据	2026-04-03 00:38:22.828292	2026-04-03 00:38:22.828292
公告详情	3	6	module_system:notice:detail	\N	\N	\N	\N	\N	f	t	f	公告详情	null	f	17	80	7bf9840f-52f4-4033-8051-975001a73d87	0	初始化数据	2026-04-03 00:38:22.828295	2026-04-03 00:38:22.828295
查询公告	3	5	module_system:notice:query	\N	\N	\N	\N	\N	f	t	f	查询公告	null	f	17	81	55dd24e2-0ab0-4ed4-b6bc-e95e56ece696	0	初始化数据	2026-04-03 00:38:22.828298	2026-04-03 00:38:22.828298
创建参数	3	1	module_system:param:create	\N	\N	\N	\N	\N	f	t	f	创建参数	null	f	18	82	9a7919b6-1685-4c91-810f-f968af6aa78c	0	初始化数据	2026-04-03 00:38:22.828301	2026-04-03 00:38:22.828301
修改参数	3	2	module_system:param:update	\N	\N	\N	\N	\N	f	t	f	修改参数	null	f	18	83	64764645-ade0-4bde-b45e-5b4cde2fa527	0	初始化数据	2026-04-03 00:38:22.828304	2026-04-03 00:38:22.828304
删除参数	3	3	module_system:param:delete	\N	\N	\N	\N	\N	f	t	f	删除参数	null	f	18	84	56c25925-f011-4e56-986e-90c61e07a6d8	0	初始化数据	2026-04-03 00:38:22.828307	2026-04-03 00:38:22.828307
导出参数	3	4	module_system:param:export	\N	\N	\N	\N	\N	f	t	f	导出参数	null	f	18	85	f5173082-51a0-4f4b-be6f-7a2c0470caa4	0	初始化数据	2026-04-03 00:38:22.82831	2026-04-03 00:38:22.82831
参数上传	3	5	module_system:param:upload	\N	\N	\N	\N	\N	f	t	f	参数上传	null	f	18	86	c21c14f2-0367-4b22-9431-c8bb3ac1b39f	0	初始化数据	2026-04-03 00:38:22.828313	2026-04-03 00:38:22.828313
参数详情	3	6	module_system:param:detail	\N	\N	\N	\N	\N	f	t	f	参数详情	null	f	18	87	042b4454-36a1-4e4b-91db-2e8af41fbc35	0	初始化数据	2026-04-03 00:38:22.828316	2026-04-03 00:38:22.828316
查询参数	3	7	module_system:param:query	\N	\N	\N	\N	\N	f	t	f	查询参数	null	f	18	88	e2a2a623-4db9-4694-912d-86b080e78d79	0	初始化数据	2026-04-03 00:38:22.828319	2026-04-03 00:38:22.828319
创建字典类型	3	1	module_system:dict_type:create	\N	\N	\N	\N	\N	f	t	f	创建字典类型	null	f	19	89	1860b824-5465-414f-98a6-03f4dd31abda	0	初始化数据	2026-04-03 00:38:22.828322	2026-04-03 00:38:22.828322
修改字典类型	3	2	module_system:dict_type:update	\N	\N	\N	\N	\N	f	t	f	修改字典类型	null	f	19	90	f5ab50f2-327b-469d-a887-5787b8beb334	0	初始化数据	2026-04-03 00:38:22.828324	2026-04-03 00:38:22.828325
删除字典类型	3	3	module_system:dict_type:delete	\N	\N	\N	\N	\N	f	t	f	删除字典类型	null	f	19	91	5caf8653-d8c4-4f22-8ba4-9435ab600808	0	初始化数据	2026-04-03 00:38:22.828328	2026-04-03 00:38:22.828329
导出字典类型	3	4	module_system:dict_type:export	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	19	92	9a1a3f53-ee36-48b1-970f-b90877341533	0	初始化数据	2026-04-03 00:38:22.828331	2026-04-03 00:38:22.828332
批量修改字典状态	3	5	module_system:dict_type:patch	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	19	93	bd15801b-edee-4265-8b8b-ceab5898a49f	0	初始化数据	2026-04-03 00:38:22.828334	2026-04-03 00:38:22.828335
字典数据查询	3	6	module_system:dict_data:query	\N	\N	\N	\N	\N	f	t	f	字典数据查询	null	f	19	94	93ca3cd4-631e-42a1-a5bc-32c1432c5fe2	0	初始化数据	2026-04-03 00:38:22.828337	2026-04-03 00:38:22.828338
创建字典数据	3	7	module_system:dict_data:create	\N	\N	\N	\N	\N	f	t	f	创建字典数据	null	f	19	95	bc812b24-97a9-4d1c-ba23-3817ca96e5ac	0	初始化数据	2026-04-03 00:38:22.82834	2026-04-03 00:38:22.82834
修改字典数据	3	8	module_system:dict_data:update	\N	\N	\N	\N	\N	f	t	f	修改字典数据	null	f	19	96	5fbf8de4-cdcf-4933-ac86-4545efcd122a	0	初始化数据	2026-04-03 00:38:22.828343	2026-04-03 00:38:22.828343
删除字典数据	3	9	module_system:dict_data:delete	\N	\N	\N	\N	\N	f	t	f	删除字典数据	null	f	19	97	8b4ce977-5913-48f5-b790-d44f234fe9c5	0	初始化数据	2026-04-03 00:38:22.828347	2026-04-03 00:38:22.828347
导出字典数据	3	10	module_system:dict_data:export	\N	\N	\N	\N	\N	f	t	f	导出字典数据	null	f	19	98	27bf104f-f194-4e7e-ae22-d3a10c08bb75	0	初始化数据	2026-04-03 00:38:22.82835	2026-04-03 00:38:22.82835
批量修改字典数据状态	3	11	module_system:dict_data:patch	\N	\N	\N	\N	\N	f	t	f	批量修改字典数据状态	null	f	19	99	555b7452-f8fe-4f54-8fb3-347c578110c0	0	初始化数据	2026-04-03 00:38:22.828353	2026-04-03 00:38:22.828353
详情字典类型	3	12	module_system:dict_type:detail	\N	\N	\N	\N	\N	f	t	f	详情字典类型	null	f	19	100	8410b781-7c89-4568-9c60-392cd3ff6cdd	0	初始化数据	2026-04-03 00:38:22.828356	2026-04-03 00:38:22.828356
查询字典类型	3	13	module_system:dict_type:query	\N	\N	\N	\N	\N	f	t	f	查询字典类型	null	f	19	101	9f2ec356-e70d-41e1-b9ce-e772b4bd40b5	0	初始化数据	2026-04-03 00:38:22.828359	2026-04-03 00:38:22.828359
详情字典数据	3	14	module_system:dict_data:detail	\N	\N	\N	\N	\N	f	t	f	详情字典数据	null	f	19	102	a530db11-7f10-4a58-bfe5-f4b5e51a976d	0	初始化数据	2026-04-03 00:38:22.828362	2026-04-03 00:38:22.828362
在线用户强制下线	3	1	module_monitor:online:delete	\N	\N	\N	\N	\N	f	t	f	在线用户强制下线	null	f	20	103	27ee0026-e2ce-4827-bb1a-0dd4f4a5be1e	0	初始化数据	2026-04-03 00:38:22.828366	2026-04-03 00:38:22.828366
清除缓存	3	1	module_monitor:cache:delete	\N	\N	\N	\N	\N	f	t	f	清除缓存	null	f	22	104	bfe4eeae-62f3-4067-8d93-0e8e1f186bcb	0	初始化数据	2026-04-03 00:38:22.828369	2026-04-03 00:38:22.828369
文件上传	3	1	module_monitor:resource:upload	\N	\N	\N	\N	\N	f	t	f	文件上传	null	f	23	105	2d5754a7-441c-441a-9206-25f89281aa0f	0	初始化数据	2026-04-03 00:38:22.828372	2026-04-03 00:38:22.828372
文件下载	3	2	module_monitor:resource:download	\N	\N	\N	\N	\N	f	t	f	文件下载	null	f	23	106	c6b70a64-9588-4473-b95e-88f73d46a4db	0	初始化数据	2026-04-03 00:38:22.828375	2026-04-03 00:38:22.828375
文件删除	3	3	module_monitor:resource:delete	\N	\N	\N	\N	\N	f	t	f	文件删除	null	f	23	107	4841ec7a-d6e0-4a29-ae5c-95a46ba80563	0	初始化数据	2026-04-03 00:38:22.828378	2026-04-03 00:38:22.828378
文件移动	3	4	module_monitor:resource:move	\N	\N	\N	\N	\N	f	t	f	文件移动	null	f	23	108	1c0ed62e-d0e2-4ce6-aea6-a1fbcc9cb3d5	0	初始化数据	2026-04-03 00:38:22.828381	2026-04-03 00:38:22.828381
文件复制	3	5	module_monitor:resource:copy	\N	\N	\N	\N	\N	f	t	f	文件复制	null	f	23	109	dd50a4a2-c269-4782-8709-f288f35347c6	0	初始化数据	2026-04-03 00:38:22.828384	2026-04-03 00:38:22.828384
文件重命名	3	6	module_monitor:resource:rename	\N	\N	\N	\N	\N	f	t	f	文件重命名	null	f	23	110	c1bc1e06-7d73-4946-afa0-9e67967ec805	0	初始化数据	2026-04-03 00:38:22.828387	2026-04-03 00:38:22.828387
创建目录	3	7	module_monitor:resource:create_dir	\N	\N	\N	\N	\N	f	t	f	创建目录	null	f	23	111	c286438d-a96f-4555-91d8-4140c99a3f2f	0	初始化数据	2026-04-03 00:38:22.828389	2026-04-03 00:38:22.82839
导出文件列表	3	9	module_monitor:resource:export	\N	\N	\N	\N	\N	f	t	f	导出文件列表	null	f	23	112	4642db40-9b02-4ea9-9c32-c5863fe5b5d2	0	初始化数据	2026-04-03 00:38:22.828392	2026-04-03 00:38:22.828393
查询代码生成业务表列表	3	1	module_generator:gencode:query	\N	\N	\N	\N	\N	f	t	f	查询代码生成业务表列表	null	f	27	113	f04b63dd-8c06-4c25-bcc5-394277c5e60f	0	查询代码生成业务表列表	2026-04-03 00:38:22.828395	2026-04-03 00:38:22.828396
创建表结构	3	2	module_generator:gencode:create	\N	\N	\N	\N	\N	f	t	f	创建表结构	null	f	27	114	1070449c-dc63-4ff3-850e-53d14d48b542	0	创建表结构	2026-04-03 00:38:22.828398	2026-04-03 00:38:22.828399
编辑业务表信息	3	3	module_generator:gencode:update	\N	\N	\N	\N	\N	f	t	f	编辑业务表信息	null	f	27	115	3d5680d1-5ab5-4d1f-a672-bb987f77386e	0	编辑业务表信息	2026-04-03 00:38:22.828401	2026-04-03 00:38:22.828402
删除业务表信息	3	4	module_generator:gencode:delete	\N	\N	\N	\N	\N	f	t	f	删除业务表信息	null	f	27	116	f74f963a-a817-47c4-9177-97b5a42c7202	0	删除业务表信息	2026-04-03 00:38:22.828404	2026-04-03 00:38:22.828405
导入表结构	3	5	module_generator:gencode:import	\N	\N	\N	\N	\N	f	t	f	导入表结构	null	f	27	117	59cf4c86-290f-43cd-9c46-a503583bb245	0	导入表结构	2026-04-03 00:38:22.828407	2026-04-03 00:38:22.828407
批量生成代码	3	6	module_generator:gencode:operate	\N	\N	\N	\N	\N	f	t	f	批量生成代码	null	f	27	118	6c6a266b-2832-402f-b165-11007f1a8968	0	批量生成代码	2026-04-03 00:38:22.82841	2026-04-03 00:38:22.82841
生成代码到指定路径	3	7	module_generator:gencode:code	\N	\N	\N	\N	\N	f	t	f	生成代码到指定路径	null	f	27	119	66c46949-9393-4f60-97fb-1a317c9bf8ed	0	生成代码到指定路径	2026-04-03 00:38:22.828413	2026-04-03 00:38:22.828413
查询数据库表列表	3	8	module_generator:dblist:query	\N	\N	\N	\N	\N	f	t	f	查询数据库表列表	null	f	27	120	8d933a04-ab62-4a88-9205-ba37dbbe0d3b	0	查询数据库表列表	2026-04-03 00:38:22.828416	2026-04-03 00:38:22.828416
同步数据库	3	9	module_generator:db:sync	\N	\N	\N	\N	\N	f	t	f	同步数据库	null	f	27	121	338ad22e-76e5-403a-a959-bf068d17ffb0	0	同步数据库	2026-04-03 00:38:22.828419	2026-04-03 00:38:22.828419
创建应用	3	1	module_application:portal:create	\N	\N	\N	\N	\N	f	t	f	创建应用	null	f	28	122	a426206a-f6a5-43c9-8c81-b12d7a42c459	0	初始化数据	2026-04-03 00:38:22.828422	2026-04-03 00:38:22.828422
修改应用	3	2	module_application:portal:update	\N	\N	\N	\N	\N	f	t	f	修改应用	null	f	28	123	3d1ef840-c0c3-4b3d-95fd-d40d7b4282f4	0	初始化数据	2026-04-03 00:38:22.828425	2026-04-03 00:38:22.828425
删除应用	3	3	module_application:portal:delete	\N	\N	\N	\N	\N	f	t	f	删除应用	null	f	28	124	1cb3fbb9-7de9-40f8-bf74-a56511e18e16	0	初始化数据	2026-04-03 00:38:22.828428	2026-04-03 00:38:22.828428
批量修改应用状态	3	4	module_application:portal:patch	\N	\N	\N	\N	\N	f	t	f	批量修改应用状态	null	f	28	125	a37f8f69-0f90-4a36-85e3-78cfefd4e9e1	0	初始化数据	2026-04-03 00:38:22.828431	2026-04-03 00:38:22.828431
详情应用	3	5	module_application:portal:detail	\N	\N	\N	\N	\N	f	t	f	详情应用	null	f	28	126	52085867-73b2-4ef8-b2b2-839a0a6c4697	0	初始化数据	2026-04-03 00:38:22.828434	2026-04-03 00:38:22.828434
查询应用	3	6	module_application:portal:query	\N	\N	\N	\N	\N	f	t	f	查询应用	null	f	28	127	df8b6a73-5041-402d-ac34-0774c229beb1	0	初始化数据	2026-04-03 00:38:22.828437	2026-04-03 00:38:22.828437
AI对话	3	1	module_ai:chat:ws	\N	\N	\N	\N	\N	f	t	f	AI对话	null	f	29	128	fd9fb4a7-2cd8-4bfd-8a99-781abf4fafed	0	AI对话	2026-04-03 00:38:22.828439	2026-04-03 00:38:22.82844
查询会话	3	2	module_ai:chat:query	\N	\N	\N	\N	\N	f	t	f	查询会话	null	f	29	129	dd4bc016-4b0c-4fc5-9561-9af61e4120ee	0	查询会话	2026-04-03 00:38:22.828443	2026-04-03 00:38:22.828443
会话详情	3	3	module_ai:chat:detail	\N	\N	\N	\N	\N	f	t	f	会话详情	null	f	29	130	a82e0084-8fce-4910-8096-fb28fa5bc7ce	0	会话详情	2026-04-03 00:38:22.828446	2026-04-03 00:38:22.828446
创建会话	3	4	module_ai:chat:create	\N	\N	\N	\N	\N	f	t	f	创建会话	null	f	29	131	51e81c58-f745-49ca-b84a-b266d3a95599	0	创建会话	2026-04-03 00:38:22.828448	2026-04-03 00:38:22.828449
更新会话	3	5	module_ai:chat:update	\N	\N	\N	\N	\N	f	t	f	更新会话	null	f	29	132	1b5024df-b0b2-4789-a752-f1f147b9baa4	0	更新会话	2026-04-03 00:38:22.828452	2026-04-03 00:38:22.828452
删除会话	3	6	module_ai:chat:delete	\N	\N	\N	\N	\N	f	t	f	删除会话	null	f	29	133	1fdc8fc7-0343-44fc-983e-a2c1f4534e6f	0	删除会话	2026-04-03 00:38:22.828454	2026-04-03 00:38:22.828455
查询会话记忆	3	1	module_ai:chat:query	\N	\N	\N	\N	\N	f	t	f	查询会话记忆	null	f	30	134	e2fe36dc-ffbd-407d-b7fc-582af63c1ece	0	查询会话记忆	2026-04-03 00:38:22.828457	2026-04-03 00:38:22.828458
会话记忆详情	3	2	module_ai:chat:detail	\N	\N	\N	\N	\N	f	t	f	会话记忆详情	null	f	30	135	e23a505a-c098-41ca-bcf4-6c62646882ad	0	会话记忆详情	2026-04-03 00:38:22.82846	2026-04-03 00:38:22.828461
删除会话记忆	3	3	module_ai:chat:delete	\N	\N	\N	\N	\N	f	t	f	删除会话记忆	null	f	30	136	f4b2ef6f-0d17-47ad-8dcd-74408b559273	0	删除会话记忆	2026-04-03 00:38:22.828463	2026-04-03 00:38:22.828464
调度器监控	2	1	module_task:cronjob:job:query	el-icon-DataLine	Job	/task/cronjob/job	module_task/cronjob/job/index	\N	f	t	f	调度器监控	null	f	31	137	bcdb67b8-95cf-4a08-a235-b01589911716	0	调度器监控	2026-04-03 00:38:22.828466	2026-04-03 00:38:22.828467
节点管理	2	2	module_task:cronjob:node:query	el-icon-Postcard	Node	/task/cronjob/node	module_task/cronjob/node/index	\N	f	t	f	节点管理	null	f	31	138	6b61fd50-a1e5-4dee-a89f-1262e76f6a04	0	节点管理	2026-04-03 00:38:22.82847	2026-04-03 00:38:22.828471
流程编排	2	1	module_task:workflow:definition:query	el-icon-SetUp	Workflow	/task/workflow/definition	module_task/workflow/definition/index	\N	f	t	f	流程编排	null	f	32	139	801ccfbc-c677-4c01-88d8-875002fefcc2	0	Vue Flow 画布与发布执行	2026-04-03 00:38:22.828473	2026-04-03 00:38:22.828474
编排节点类型	2	2	module_task:workflow:node-type:query	el-icon-Grid	WorkflowNodeType	/task/workflow/node-type	module_task/workflow/node-type/index	\N	f	t	f	编排节点类型	null	f	32	140	b8681195-1acc-4051-b751-1ebb160ebf3f	0	画布节点类型与 Prefect 执行逻辑	2026-04-03 00:38:22.828476	2026-04-03 00:38:22.828476
创建示例	3	1	module_example:demo:create	\N	\N	\N	\N	\N	f	t	f	创建示例	null	f	33	141	67875dc1-a37c-4b04-91d0-91bf0dae0a0f	0	初始化数据	2026-04-03 00:38:22.828479	2026-04-03 00:38:22.828479
更新示例	3	2	module_example:demo:update	\N	\N	\N	\N	\N	f	t	f	更新示例	null	f	33	142	20178868-4794-464b-957b-53da5bfc54f1	0	初始化数据	2026-04-03 00:38:22.828482	2026-04-03 00:38:22.828482
删除示例	3	3	module_example:demo:delete	\N	\N	\N	\N	\N	f	t	f	删除示例	null	f	33	143	59d78bc1-9b03-4639-9ded-30c5752361dc	0	初始化数据	2026-04-03 00:38:22.828485	2026-04-03 00:38:22.828485
批量修改示例状态	3	4	module_example:demo:patch	\N	\N	\N	\N	\N	f	t	f	批量修改示例状态	null	f	33	144	06b8aaba-cee1-4ccd-a43d-6baeaa9b854c	0	初始化数据	2026-04-03 00:38:22.828488	2026-04-03 00:38:22.828488
导出示例	3	5	module_example:demo:export	\N	\N	\N	\N	\N	f	t	f	导出示例	null	f	33	145	22697978-eb66-45c6-b954-762dc4c81ac5	0	初始化数据	2026-04-03 00:38:22.828491	2026-04-03 00:38:22.828491
导入示例	3	6	module_example:demo:import	\N	\N	\N	\N	\N	f	t	f	导入示例	null	f	33	146	233034b2-a921-46f8-8490-7787e46eae4f	0	初始化数据	2026-04-03 00:38:22.828494	2026-04-03 00:38:22.828494
下载导入示例模版	3	7	module_example:demo:download	\N	\N	\N	\N	\N	f	t	f	下载导入示例模版	null	f	33	147	959afc8a-ecdf-496b-aa61-ab95db2821b7	0	初始化数据	2026-04-03 00:38:22.828497	2026-04-03 00:38:22.828497
详情示例	3	8	module_example:demo:detail	\N	\N	\N	\N	\N	f	t	f	详情示例	null	f	33	148	47df5b9c-9678-4630-a67a-18d4f39747fa	0	初始化数据	2026-04-03 00:38:22.8285	2026-04-03 00:38:22.8285
查询示例	3	9	module_example:demo:query	\N	\N	\N	\N	\N	f	t	f	查询示例	null	f	33	149	6e8189e0-0dad-4e1e-b310-3f8921635951	0	初始化数据	2026-04-03 00:38:22.828503	2026-04-03 00:38:22.828503
三级菜单	2	1	module_example:demo01:query	menu	Demo01	/example/demo-group/demo01	module_example/demo01/index	\N	f	t	f	三级菜单	null	f	34	150	59c4f878-dcbe-44a0-8955-31c9c254104e	0	示例01管理	2026-04-03 00:38:22.828506	2026-04-03 00:38:22.828506
查询调度器	3	1	module_task:cronjob:job:query	\N	\N	\N	\N	\N	f	t	f	查询调度器	null	f	137	151	61944926-cb21-4929-8c9c-7beebc890d22	0	查询调度器	2026-04-03 00:38:22.834804	2026-04-03 00:38:22.834806
控制调度器	3	2	module_task:cronjob:job:scheduler	\N	\N	\N	\N	\N	f	t	f	控制调度器	null	f	137	152	95bd91d9-5681-42f6-8b70-2ae0af9d5c79	0	控制调度器	2026-04-03 00:38:22.83481	2026-04-03 00:38:22.834811
操作任务	3	3	module_task:cronjob:job:task	\N	\N	\N	\N	\N	f	t	f	操作任务	null	f	137	153	bc2813c4-f168-49a0-8a94-817a8e305fab	0	操作任务	2026-04-03 00:38:22.834814	2026-04-03 00:38:22.834814
删除执行日志	3	4	module_task:cronjob:job:delete	\N	\N	\N	\N	\N	f	t	f	删除执行日志	null	f	137	154	f2172496-bc2f-4385-99c1-4791000468a4	0	删除执行日志	2026-04-03 00:38:22.834817	2026-04-03 00:38:22.834818
详情执行日志	3	5	module_task:cronjob:job:detail	\N	\N	\N	\N	\N	f	t	f	详情执行日志	null	f	137	155	50701a79-e502-4cef-928f-c91cd03b8915	0	详情执行日志	2026-04-03 00:38:22.834821	2026-04-03 00:38:22.834821
创建节点	3	1	module_task:cronjob:node:create	\N	\N	\N	\N	\N	f	t	f	创建节点	null	f	138	156	403ebc5e-bb5c-42c1-8c5a-cb6b90702174	0	创建节点	2026-04-03 00:38:22.834824	2026-04-03 00:38:22.834824
调试节点	3	2	module_task:cronjob:node:execute	\N	\N	\N	\N	\N	f	t	f	调试节点	null	f	138	157	8a62c71d-dd08-4278-a5a2-fc59b645ab25	0	调试节点	2026-04-03 00:38:22.834827	2026-04-03 00:38:22.834828
修改节点	3	3	module_task:cronjob:node:update	\N	\N	\N	\N	\N	f	t	f	修改节点	null	f	138	158	d14eb6ff-9e68-420b-b5bb-0b6035653b6e	0	修改节点	2026-04-03 00:38:22.83483	2026-04-03 00:38:22.834831
删除节点	3	4	module_task:cronjob:node:delete	\N	\N	\N	\N	\N	f	t	f	删除节点	null	f	138	159	d777a930-a4a9-435f-98c5-f86e74de18b7	0	删除节点	2026-04-03 00:38:22.834833	2026-04-03 00:38:22.834834
详情节点	3	5	module_task:cronjob:node:detail	\N	\N	\N	\N	\N	f	t	f	详情节点	null	f	138	160	02a20050-a386-4e89-991f-72abd241a67f	0	详情节点	2026-04-03 00:38:22.834837	2026-04-03 00:38:22.834838
查询节点	3	6	module_task:cronjob:node:query	\N	\N	\N	\N	\N	f	t	f	查询节点	null	f	138	161	f053043e-33e5-4cbc-a171-75b8621e3b61	0	查询节点	2026-04-03 00:38:22.83484	2026-04-03 00:38:22.834841
创建流程	3	1	module_task:workflow:definition:create	\N	\N	\N	\N	\N	f	t	f	创建流程	null	f	139	162	42c76534-0cfe-433f-be15-96bf53915ea0	0	创建流程	2026-04-03 00:38:22.834843	2026-04-03 00:38:22.834844
执行流程	3	2	module_task:workflow:definition:execute	\N	\N	\N	\N	\N	f	t	f	执行流程	null	f	139	163	72ef065a-3751-4df7-a4b8-6bf39c109fd7	0	执行流程	2026-04-03 00:38:22.834846	2026-04-03 00:38:22.834847
修改流程	3	3	module_task:workflow:definition:update	\N	\N	\N	\N	\N	f	t	f	修改流程	null	f	139	164	f40c9482-5293-44e2-80f9-65322d768d7a	0	修改流程	2026-04-03 00:38:22.83485	2026-04-03 00:38:22.83485
删除流程	3	4	module_task:workflow:definition:delete	\N	\N	\N	\N	\N	f	t	f	删除流程	null	f	139	165	1a54d0cd-0853-4457-8b53-1db2e3be6ff6	0	删除流程	2026-04-03 00:38:22.834853	2026-04-03 00:38:22.834853
详情流程	3	5	module_task:workflow:definition:detail	\N	\N	\N	\N	\N	f	t	f	详情流程	null	f	139	166	b75315f7-f00d-4cd2-bfbd-f859cf411565	0	详情流程	2026-04-03 00:38:22.834856	2026-04-03 00:38:22.834856
查询流程	3	6	module_task:workflow:definition:query	\N	\N	\N	\N	\N	f	t	f	查询流程	null	f	139	167	93bde336-0472-460f-9144-eb327d92eaeb	0	查询流程	2026-04-03 00:38:22.834859	2026-04-03 00:38:22.834859
创建编排节点类型	3	1	module_task:workflow:node-type:create	\N	\N	\N	\N	\N	f	t	f	创建编排节点类型	null	f	140	168	99ed4d1b-8a4b-4fbd-8b26-c126b1934bf2	0	创建编排节点类型	2026-04-03 00:38:22.834862	2026-04-03 00:38:22.834863
修改编排节点类型	3	2	module_task:workflow:node-type:update	\N	\N	\N	\N	\N	f	t	f	修改编排节点类型	null	f	140	169	a126b8d0-484a-419a-b811-1ec240ed36ef	0	修改编排节点类型	2026-04-03 00:38:22.834865	2026-04-03 00:38:22.834866
删除编排节点类型	3	3	module_task:workflow:node-type:delete	\N	\N	\N	\N	\N	f	t	f	删除编排节点类型	null	f	140	170	511ef043-2ee9-40f0-9df4-a316f61e2f53	0	删除编排节点类型	2026-04-03 00:38:22.834869	2026-04-03 00:38:22.834869
详情编排节点类型	3	4	module_task:workflow:node-type:detail	\N	\N	\N	\N	\N	f	t	f	详情编排节点类型	null	f	140	171	c1c6cbe2-9a82-42cf-9940-c6afa1b75c06	0	详情编排节点类型	2026-04-03 00:38:22.834872	2026-04-03 00:38:22.834872
查询编排节点类型	3	5	module_task:workflow:node-type:query	\N	\N	\N	\N	\N	f	t	f	查询编排节点类型	null	f	140	172	bc8d7df6-25f1-4f51-9f10-2d5103f423ac	0	查询编排节点类型	2026-04-03 00:38:22.834875	2026-04-03 00:38:22.834875
创建示例01	3	1	module_example:demo01:create	\N	\N	\N	\N	\N	f	t	f	创建示例01	null	f	150	173	9fc5653a-d558-474a-a548-66f3639063c9	0	初始化数据	2026-04-03 00:38:22.834878	2026-04-03 00:38:22.834878
更新示例01	3	2	module_example:demo01:update	\N	\N	\N	\N	\N	f	t	f	更新示例01	null	f	150	174	8b9c3417-41c2-4cdf-ac90-8b0bd5377970	0	初始化数据	2026-04-03 00:38:22.834881	2026-04-03 00:38:22.834881
删除示例01	3	3	module_example:demo01:delete	\N	\N	\N	\N	\N	f	t	f	删除示例01	null	f	150	175	a0014329-1fca-464d-9d35-3932ca151a09	0	初始化数据	2026-04-03 00:38:22.834884	2026-04-03 00:38:22.834884
批量修改示例01状态	3	4	module_example:demo01:patch	\N	\N	\N	\N	\N	f	t	f	批量修改示例01状态	null	f	150	176	2a6be91a-a713-4c2b-8ca1-b99ef89ebe0b	0	初始化数据	2026-04-03 00:38:22.834887	2026-04-03 00:38:22.834887
导出示例01	3	5	module_example:demo01:export	\N	\N	\N	\N	\N	f	t	f	导出示例01	null	f	150	177	5d1cbc81-6820-45a4-8347-40c62a18957b	0	初始化数据	2026-04-03 00:38:22.83489	2026-04-03 00:38:22.834891
导入示例01	3	6	module_example:demo01:import	\N	\N	\N	\N	\N	f	t	f	导入示例01	null	f	150	178	4bd21e9e-285d-4441-9e96-e311a29ef9fc	0	初始化数据	2026-04-03 00:38:22.834894	2026-04-03 00:38:22.834894
下载导入示例01模版	3	7	module_example:demo01:download	\N	\N	\N	\N	\N	f	t	f	下载导入示例01模版	null	f	150	179	d81dca7c-0c30-4254-b696-f9b0f91cd896	0	初始化数据	2026-04-03 00:38:22.834897	2026-04-03 00:38:22.834897
详情示例01	3	8	module_example:demo01:detail	\N	\N	\N	\N	\N	f	t	f	详情示例01	null	f	150	180	456c3500-5fb4-49cb-9612-e7905b133142	0	初始化数据	2026-04-03 00:38:22.8349	2026-04-03 00:38:22.8349
查询示例01	3	9	module_example:demo01:query	\N	\N	\N	\N	\N	f	t	f	查询示例01	null	f	150	181	17a07a9e-8786-434b-95b8-47acfd6ea4e7	0	初始化数据	2026-04-03 00:38:22.834903	2026-04-03 00:38:22.834903
\.


--
-- Data for Name: sys_notice; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_notice (notice_title, notice_type, notice_content, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_param; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_param (config_name, config_key, config_value, config_type, id, uuid, status, description, created_time, updated_time) FROM stdin;
网站名称	sys_web_title	FastApiAdmin	t	1	832c89cb-d562-4f5f-bb0d-1414d14dbf13	0	初始化数据	2026-04-03 00:38:22.840724	2026-04-03 00:38:22.840725
网站描述	sys_web_description	FastApiAdmin 是完全开源的权限管理系统	t	2	cb3aa6ca-cd34-4853-a9dc-c8f5359fd737	0	初始化数据	2026-04-03 00:38:22.840729	2026-04-03 00:38:22.840729
网页图标	sys_web_favicon	https://service.fastapiadmin.com/api/v1/static/image/favicon.png	t	3	af8fb26f-5c11-421d-8866-0abfb3f82ca8	0	初始化数据	2026-04-03 00:38:22.840732	2026-04-03 00:38:22.840732
网站Logo	sys_web_logo	https://service.fastapiadmin.com/api/v1/static/image/logo.png	t	4	368214e2-f00a-4e63-8eef-c9093902b307	0	初始化数据	2026-04-03 00:38:22.840735	2026-04-03 00:38:22.840736
登录背景	sys_login_background	https://service.fastapiadmin.com/api/v1/static/image/background.svg	t	5	6331cd2b-33c3-44a1-b2ab-ceec96e00b46	0	初始化数据	2026-04-03 00:38:22.840738	2026-04-03 00:38:22.840739
版权信息	sys_web_copyright	Copyright © 2025-2026 service.fastapiadmin.com 版权所有	t	6	d893f6fd-cfee-4eae-b616-dc632ac97431	0	初始化数据	2026-04-03 00:38:22.840741	2026-04-03 00:38:22.840742
备案信息	sys_keep_record	陕ICP备2025069493号-1	t	7	89727f04-6946-4fde-bbb1-569eff9b45ac	0	初始化数据	2026-04-03 00:38:22.840744	2026-04-03 00:38:22.840744
帮助文档	sys_help_doc	https://service.fastapiadmin.com	t	8	498769ce-dee0-42c6-b933-2de470076272	0	初始化数据	2026-04-03 00:38:22.840747	2026-04-03 00:38:22.840747
隐私政策	sys_web_privacy	https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE	t	9	d22ccc8c-ddf4-4fe7-82f2-cde2602f6437	0	初始化数据	2026-04-03 00:38:22.84075	2026-04-03 00:38:22.84075
用户协议	sys_web_clause	https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE	t	10	fedf51ac-7a32-4e77-ae6a-b36992d17327	0	初始化数据	2026-04-03 00:38:22.840753	2026-04-03 00:38:22.840753
源码代码	sys_git_code	https://github.com/fastapiadmin/FastapiAdmin.git	t	11	8d5c0934-971d-4542-95a2-089961dbcc47	0	初始化数据	2026-04-03 00:38:22.840756	2026-04-03 00:38:22.840756
项目版本	sys_web_version	2.0.0	t	12	eab70dad-501c-419d-b251-64c5409c4fac	0	初始化数据	2026-04-03 00:38:22.840758	2026-04-03 00:38:22.840759
演示模式启用	demo_enable	false	t	13	def391b0-7050-4167-8909-17d458b56db8	0	初始化数据	2026-04-03 00:38:22.840761	2026-04-03 00:38:22.840762
演示访问IP白名单	ip_white_list	["127.0.0.1"]	t	14	8722deeb-2950-4e1d-8275-25da9ca57189	0	初始化数据	2026-04-03 00:38:22.840764	2026-04-03 00:38:22.840765
接口白名单	white_api_list_path	["/api/v1/system/auth/login", "/api/v1/system/auth/token/refresh", "/api/v1/system/auth/captcha/get", "/api/v1/system/auth/logout", "/api/v1/system/config/info", "/api/v1/system/user/current/info", "/api/v1/system/notice/available", "/api/v1/system/auth/auto-login/users", "/api/v1/system/auth/auto-login/token", "/api/v1/system/auth/auto-login"]	t	15	1c2a8d35-2bb8-4309-940e-8796e90b3c60	0	初始化数据	2026-04-03 00:38:22.840767	2026-04-03 00:38:22.840767
访问IP黑名单	ip_black_list	[]	t	16	b46b6456-b481-4034-8fa4-bb9b8a750a64	0	初始化数据	2026-04-03 00:38:22.84077	2026-04-03 00:38:22.84077
调度器状态	scheduler_status	stopped	t	17	e52b6183-8e46-4d75-8b24-e3341c5058ac	0	\N	2026-04-03 00:38:32.994452	2026-04-03 00:38:32.994455
\.


--
-- Data for Name: sys_position; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_position (name, "order", id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_role; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_role (name, code, "order", data_scope, id, uuid, status, description, created_time, updated_time) FROM stdin;
管理员角色	ADMIN	1	4	1	0a3eef5e-7d6e-4e6a-aa0b-3fc4ccb27d6a	0	初始化角色	2026-04-03 00:38:22.847925	2026-04-03 00:38:22.847926
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
-- Data for Name: sys_user; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_user (username, password, name, mobile, email, gender, avatar, is_superuser, last_login, gitee_login, github_login, wx_login, qq_login, dept_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
admin	$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa	超级管理员	\N	\N	0	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	t	\N	\N	\N	\N	\N	1	1	98e27ecc-32c6-4c2d-93ca-9cfcf79ab742	0	超级管理员	2026-04-03 00:38:22.863379	2026-04-03 00:38:22.86338	\N	\N
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
\.


--
-- Data for Name: task_job; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.task_job (job_id, job_name, trigger_type, status, next_run_time, job_state, result, error, id, uuid, description, created_time, updated_time) FROM stdin;
\.


--
-- Data for Name: task_node; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.task_node (name, code, jobstore, executor, trigger, trigger_args, func, args, kwargs, "coalesce", max_instances, start_date, end_date, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: task_workflow; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.task_workflow (name, code, workflow_status, nodes, edges, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: task_workflow_node_type; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.task_workflow_node_type (name, code, category, func, args, kwargs, sort_order, is_active, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Name: app_portal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.app_portal_id_seq', 1, false);


--
-- Name: gen_demo01_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.gen_demo01_id_seq', 1, false);


--
-- Name: gen_demo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.gen_demo_id_seq', 1, false);


--
-- Name: gen_table_column_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.gen_table_column_id_seq', 1, false);


--
-- Name: gen_table_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.gen_table_id_seq', 1, false);


--
-- Name: sys_dept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_dept_id_seq', 1, true);


--
-- Name: sys_dict_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_dict_data_id_seq', 34, true);


--
-- Name: sys_dict_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_dict_type_id_seq', 10, true);


--
-- Name: sys_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_log_id_seq', 1, false);


--
-- Name: sys_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_menu_id_seq', 181, true);


--
-- Name: sys_notice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_notice_id_seq', 1, false);


--
-- Name: sys_param_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_param_id_seq', 17, true);


--
-- Name: sys_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_position_id_seq', 1, false);


--
-- Name: sys_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_role_id_seq', 1, true);


--
-- Name: sys_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_user_id_seq', 1, true);


--
-- Name: task_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.task_job_id_seq', 1, false);


--
-- Name: task_node_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.task_node_id_seq', 1, false);


--
-- Name: task_workflow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.task_workflow_id_seq', 1, false);


--
-- Name: task_workflow_node_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.task_workflow_node_type_id_seq', 1, false);


--
-- Name: agno_schema_versions agno_schema_versions_pkey; Type: CONSTRAINT; Schema: ai; Owner: root
--

ALTER TABLE ONLY ai.agno_schema_versions
    ADD CONSTRAINT agno_schema_versions_pkey PRIMARY KEY (table_name);


--
-- Name: agno_sessions agno_sessions_pkey; Type: CONSTRAINT; Schema: ai; Owner: root
--

ALTER TABLE ONLY ai.agno_sessions
    ADD CONSTRAINT agno_sessions_pkey PRIMARY KEY (session_id);


--
-- Name: app_portal app_portal_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.app_portal
    ADD CONSTRAINT app_portal_pkey PRIMARY KEY (id);


--
-- Name: apscheduler_jobs apscheduler_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.apscheduler_jobs
    ADD CONSTRAINT apscheduler_jobs_pkey PRIMARY KEY (id);


--
-- Name: gen_demo01 gen_demo01_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_demo01
    ADD CONSTRAINT gen_demo01_pkey PRIMARY KEY (id);


--
-- Name: gen_demo gen_demo_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_demo
    ADD CONSTRAINT gen_demo_pkey PRIMARY KEY (id);


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
-- Name: sys_dept sys_dept_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_pkey PRIMARY KEY (id);


--
-- Name: sys_dict_data sys_dict_data_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_pkey PRIMARY KEY (id);


--
-- Name: sys_dict_type sys_dict_type_dict_type_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_type
    ADD CONSTRAINT sys_dict_type_dict_type_key UNIQUE (dict_type);


--
-- Name: sys_dict_type sys_dict_type_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_type
    ADD CONSTRAINT sys_dict_type_pkey PRIMARY KEY (id);


--
-- Name: sys_log sys_log_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_pkey PRIMARY KEY (id);


--
-- Name: sys_menu sys_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_menu
    ADD CONSTRAINT sys_menu_pkey PRIMARY KEY (id);


--
-- Name: sys_notice sys_notice_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_pkey PRIMARY KEY (id);


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
-- Name: sys_user sys_user_email_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_email_key UNIQUE (email);


--
-- Name: sys_user sys_user_mobile_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_mobile_key UNIQUE (mobile);


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
-- Name: sys_user sys_user_username_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_username_key UNIQUE (username);


--
-- Name: task_job task_job_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_job
    ADD CONSTRAINT task_job_pkey PRIMARY KEY (id);


--
-- Name: task_node task_node_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_code_key UNIQUE (code);


--
-- Name: task_node task_node_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_pkey PRIMARY KEY (id);


--
-- Name: task_workflow_node_type task_workflow_node_type_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type
    ADD CONSTRAINT task_workflow_node_type_code_key UNIQUE (code);


--
-- Name: task_workflow_node_type task_workflow_node_type_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type
    ADD CONSTRAINT task_workflow_node_type_pkey PRIMARY KEY (id);


--
-- Name: task_workflow task_workflow_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT task_workflow_pkey PRIMARY KEY (id);


--
-- Name: task_workflow uq_task_workflow_code; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT uq_task_workflow_code UNIQUE (code);


--
-- Name: idx_agno_schema_versions_created_at; Type: INDEX; Schema: ai; Owner: root
--

CREATE INDEX idx_agno_schema_versions_created_at ON ai.agno_schema_versions USING btree (created_at);


--
-- Name: idx_agno_sessions_created_at; Type: INDEX; Schema: ai; Owner: root
--

CREATE INDEX idx_agno_sessions_created_at ON ai.agno_sessions USING btree (created_at);


--
-- Name: idx_agno_sessions_session_type; Type: INDEX; Schema: ai; Owner: root
--

CREATE INDEX idx_agno_sessions_session_type ON ai.agno_sessions USING btree (session_type);


--
-- Name: ix_app_portal_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_app_portal_created_id ON public.app_portal USING btree (created_id);


--
-- Name: ix_app_portal_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_app_portal_created_time ON public.app_portal USING btree (created_time);


--
-- Name: ix_app_portal_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_app_portal_id ON public.app_portal USING btree (id);


--
-- Name: ix_app_portal_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_app_portal_status ON public.app_portal USING btree (status);


--
-- Name: ix_app_portal_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_app_portal_updated_id ON public.app_portal USING btree (updated_id);


--
-- Name: ix_app_portal_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_app_portal_updated_time ON public.app_portal USING btree (updated_time);


--
-- Name: ix_app_portal_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_app_portal_uuid ON public.app_portal USING btree (uuid);


--
-- Name: ix_apscheduler_jobs_next_run_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_apscheduler_jobs_next_run_time ON public.apscheduler_jobs USING btree (next_run_time);


--
-- Name: ix_gen_demo01_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo01_created_id ON public.gen_demo01 USING btree (created_id);


--
-- Name: ix_gen_demo01_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo01_created_time ON public.gen_demo01 USING btree (created_time);


--
-- Name: ix_gen_demo01_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo01_id ON public.gen_demo01 USING btree (id);


--
-- Name: ix_gen_demo01_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo01_status ON public.gen_demo01 USING btree (status);


--
-- Name: ix_gen_demo01_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo01_updated_id ON public.gen_demo01 USING btree (updated_id);


--
-- Name: ix_gen_demo01_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo01_updated_time ON public.gen_demo01 USING btree (updated_time);


--
-- Name: ix_gen_demo01_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_gen_demo01_uuid ON public.gen_demo01 USING btree (uuid);


--
-- Name: ix_gen_demo_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo_created_id ON public.gen_demo USING btree (created_id);


--
-- Name: ix_gen_demo_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo_created_time ON public.gen_demo USING btree (created_time);


--
-- Name: ix_gen_demo_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo_id ON public.gen_demo USING btree (id);


--
-- Name: ix_gen_demo_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo_status ON public.gen_demo USING btree (status);


--
-- Name: ix_gen_demo_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo_updated_id ON public.gen_demo USING btree (updated_id);


--
-- Name: ix_gen_demo_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_demo_updated_time ON public.gen_demo USING btree (updated_time);


--
-- Name: ix_gen_demo_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_gen_demo_uuid ON public.gen_demo USING btree (uuid);


--
-- Name: ix_gen_table_column_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_created_id ON public.gen_table_column USING btree (created_id);


--
-- Name: ix_gen_table_column_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_created_time ON public.gen_table_column USING btree (created_time);


--
-- Name: ix_gen_table_column_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_id ON public.gen_table_column USING btree (id);


--
-- Name: ix_gen_table_column_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_status ON public.gen_table_column USING btree (status);


--
-- Name: ix_gen_table_column_table_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_column_table_id ON public.gen_table_column USING btree (table_id);


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
-- Name: ix_gen_table_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_id ON public.gen_table USING btree (id);


--
-- Name: ix_gen_table_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_gen_table_status ON public.gen_table USING btree (status);


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
-- Name: ix_sys_dept_code; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_code ON public.sys_dept USING btree (code);


--
-- Name: ix_sys_dept_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_created_time ON public.sys_dept USING btree (created_time);


--
-- Name: ix_sys_dept_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_id ON public.sys_dept USING btree (id);


--
-- Name: ix_sys_dept_parent_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_parent_id ON public.sys_dept USING btree (parent_id);


--
-- Name: ix_sys_dept_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dept_status ON public.sys_dept USING btree (status);


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
-- Name: ix_sys_dict_data_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_data_id ON public.sys_dict_data USING btree (id);


--
-- Name: ix_sys_dict_data_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_data_status ON public.sys_dict_data USING btree (status);


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
-- Name: ix_sys_dict_type_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_type_id ON public.sys_dict_type USING btree (id);


--
-- Name: ix_sys_dict_type_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_type_status ON public.sys_dict_type USING btree (status);


--
-- Name: ix_sys_dict_type_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_dict_type_updated_time ON public.sys_dict_type USING btree (updated_time);


--
-- Name: ix_sys_dict_type_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_dict_type_uuid ON public.sys_dict_type USING btree (uuid);


--
-- Name: ix_sys_log_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_log_created_id ON public.sys_log USING btree (created_id);


--
-- Name: ix_sys_log_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_log_created_time ON public.sys_log USING btree (created_time);


--
-- Name: ix_sys_log_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_log_id ON public.sys_log USING btree (id);


--
-- Name: ix_sys_log_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_log_status ON public.sys_log USING btree (status);


--
-- Name: ix_sys_log_updated_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_log_updated_id ON public.sys_log USING btree (updated_id);


--
-- Name: ix_sys_log_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_log_updated_time ON public.sys_log USING btree (updated_time);


--
-- Name: ix_sys_log_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_log_uuid ON public.sys_log USING btree (uuid);


--
-- Name: ix_sys_menu_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_menu_created_time ON public.sys_menu USING btree (created_time);


--
-- Name: ix_sys_menu_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_menu_id ON public.sys_menu USING btree (id);


--
-- Name: ix_sys_menu_parent_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_menu_parent_id ON public.sys_menu USING btree (parent_id);


--
-- Name: ix_sys_menu_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_menu_status ON public.sys_menu USING btree (status);


--
-- Name: ix_sys_menu_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_menu_updated_time ON public.sys_menu USING btree (updated_time);


--
-- Name: ix_sys_menu_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_menu_uuid ON public.sys_menu USING btree (uuid);


--
-- Name: ix_sys_notice_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_created_id ON public.sys_notice USING btree (created_id);


--
-- Name: ix_sys_notice_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_created_time ON public.sys_notice USING btree (created_time);


--
-- Name: ix_sys_notice_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_id ON public.sys_notice USING btree (id);


--
-- Name: ix_sys_notice_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_notice_status ON public.sys_notice USING btree (status);


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
-- Name: ix_sys_param_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_created_time ON public.sys_param USING btree (created_time);


--
-- Name: ix_sys_param_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_id ON public.sys_param USING btree (id);


--
-- Name: ix_sys_param_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_param_status ON public.sys_param USING btree (status);


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
-- Name: ix_sys_position_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_id ON public.sys_position USING btree (id);


--
-- Name: ix_sys_position_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_position_status ON public.sys_position USING btree (status);


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
-- Name: ix_sys_role_code; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_code ON public.sys_role USING btree (code);


--
-- Name: ix_sys_role_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_created_time ON public.sys_role USING btree (created_time);


--
-- Name: ix_sys_role_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_id ON public.sys_role USING btree (id);


--
-- Name: ix_sys_role_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_status ON public.sys_role USING btree (status);


--
-- Name: ix_sys_role_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_role_updated_time ON public.sys_role USING btree (updated_time);


--
-- Name: ix_sys_role_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_role_uuid ON public.sys_role USING btree (uuid);


--
-- Name: ix_sys_user_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_created_id ON public.sys_user USING btree (created_id);


--
-- Name: ix_sys_user_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_created_time ON public.sys_user USING btree (created_time);


--
-- Name: ix_sys_user_dept_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_dept_id ON public.sys_user USING btree (dept_id);


--
-- Name: ix_sys_user_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_id ON public.sys_user USING btree (id);


--
-- Name: ix_sys_user_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_user_status ON public.sys_user USING btree (status);


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
-- Name: ix_task_job_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_job_id ON public.task_job USING btree (id);


--
-- Name: ix_task_job_job_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_job_job_id ON public.task_job USING btree (job_id);


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
-- Name: ix_task_node_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_id ON public.task_node USING btree (id);


--
-- Name: ix_task_node_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_node_status ON public.task_node USING btree (status);


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
-- Name: ix_task_workflow_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_id ON public.task_workflow USING btree (id);


--
-- Name: ix_task_workflow_node_type_created_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_created_id ON public.task_workflow_node_type USING btree (created_id);


--
-- Name: ix_task_workflow_node_type_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_created_time ON public.task_workflow_node_type USING btree (created_time);


--
-- Name: ix_task_workflow_node_type_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_id ON public.task_workflow_node_type USING btree (id);


--
-- Name: ix_task_workflow_node_type_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_task_workflow_node_type_status ON public.task_workflow_node_type USING btree (status);


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
-- Name: app_portal app_portal_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.app_portal
    ADD CONSTRAINT app_portal_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_portal app_portal_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.app_portal
    ADD CONSTRAINT app_portal_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_demo01 gen_demo01_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_demo01
    ADD CONSTRAINT gen_demo01_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_demo01 gen_demo01_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_demo01
    ADD CONSTRAINT gen_demo01_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_demo gen_demo_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_demo
    ADD CONSTRAINT gen_demo_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_demo gen_demo_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_demo
    ADD CONSTRAINT gen_demo_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table_column gen_table_column_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table_column gen_table_column_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.gen_table(id) ON DELETE CASCADE;


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
-- Name: gen_table gen_table_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dept sys_dept_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.sys_dept(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dict_data sys_dict_data_dict_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_dict_type_id_fkey FOREIGN KEY (dict_type_id) REFERENCES public.sys_dict_type(id) ON DELETE CASCADE;


--
-- Name: sys_log sys_log_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_log sys_log_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_menu sys_menu_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_menu
    ADD CONSTRAINT sys_menu_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.sys_menu(id) ON DELETE SET NULL;


--
-- Name: sys_notice sys_notice_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_notice sys_notice_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_position sys_position_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_position sys_position_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


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
    ADD CONSTRAINT sys_role_menus_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.sys_menu(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role_menus sys_role_menus_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role_menus
    ADD CONSTRAINT sys_role_menus_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.sys_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user sys_user_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


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
-- Name: sys_user sys_user_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_node task_node_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_node
    ADD CONSTRAINT task_node_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


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
-- Name: task_workflow_node_type task_workflow_node_type_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type
    ADD CONSTRAINT task_workflow_node_type_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_workflow_node_type task_workflow_node_type_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow_node_type
    ADD CONSTRAINT task_workflow_node_type_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: task_workflow task_workflow_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.task_workflow
    ADD CONSTRAINT task_workflow_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

\unrestrict ZPSb5Q9rvfnfbn6VdXJ2edWyHcIou9jw4hZaoDETBqBWj7T0xI08ijcpb6b4BKi

