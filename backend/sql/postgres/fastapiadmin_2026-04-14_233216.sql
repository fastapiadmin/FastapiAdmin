--
-- PostgreSQL database dump
--

\restrict MSeJP5WlbZL9YuY2N0b0zn88F8HQRuiwqrwhSdt3h8bn3cZtyhxMSVH7wTian01

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
    tenant_id integer NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.app_portal OWNER TO root;

--
-- Name: TABLE app_portal; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.app_portal IS '门户应用';


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
-- Name: COLUMN app_portal.tenant_id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.app_portal.tenant_id IS '租户ID';


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
    code character varying(16) NOT NULL,
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
    code character varying(16) NOT NULL,
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
-- Name: sys_tenant; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.sys_tenant (
    name character varying(100) NOT NULL,
    code character varying(100) NOT NULL,
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_tenant OWNER TO root;

--
-- Name: TABLE sys_tenant; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON TABLE public.sys_tenant IS '租户表';


--
-- Name: COLUMN sys_tenant.name; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_tenant.name IS '租户名称';


--
-- Name: COLUMN sys_tenant.code; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_tenant.code IS '租户编码';


--
-- Name: COLUMN sys_tenant.start_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_tenant.start_time IS '开始时间';


--
-- Name: COLUMN sys_tenant.end_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_tenant.end_time IS '结束时间';


--
-- Name: COLUMN sys_tenant.id; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_tenant.id IS '主键ID';


--
-- Name: COLUMN sys_tenant.uuid; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_tenant.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_tenant.status; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_tenant.status IS '状态(0:正常 1:禁用)';


--
-- Name: COLUMN sys_tenant.description; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_tenant.description IS '备注/描述';


--
-- Name: COLUMN sys_tenant.created_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_tenant.created_time IS '创建时间';


--
-- Name: COLUMN sys_tenant.updated_time; Type: COMMENT; Schema: public; Owner: root
--

COMMENT ON COLUMN public.sys_tenant.updated_time IS '更新时间';


--
-- Name: sys_tenant_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.sys_tenant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_tenant_id_seq OWNER TO root;

--
-- Name: sys_tenant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.sys_tenant_id_seq OWNED BY public.sys_tenant.id;


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
    tenant_id integer NOT NULL,
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
-- Name: sys_tenant id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_tenant ALTER COLUMN id SET DEFAULT nextval('public.sys_tenant_id_seq'::regclass);


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

COPY public.app_portal (name, access_url, icon_url, id, uuid, status, description, created_time, updated_time, tenant_id, created_id, updated_id) FROM stdin;
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
集团总公司	1	GROUP	部门负责人	1582112620	deptadmin@example.com	\N	1	e7ea04a1-99dc-4f09-a7e4-4e86b7c3d9e0	0	集团总公司	2026-04-14 23:31:02.186136	2026-04-14 23:31:02.186143
\.


--
-- Data for Name: sys_dict_data; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_dict_data (dict_sort, dict_label, dict_value, css_class, list_class, is_default, dict_type, dict_type_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
1	男	0	blue	\N	t	sys_user_sex	1	1	ee0e5897-2b41-4b60-beaa-b9ea7457d303	0	性别男	2026-04-14 23:31:02.199401	2026-04-14 23:31:02.199405
2	女	1	pink	\N	f	sys_user_sex	1	2	66901d52-15e7-4c6c-8f7b-012ec483b875	0	性别女	2026-04-14 23:31:02.19941	2026-04-14 23:31:02.19941
3	未知	2	red	\N	f	sys_user_sex	1	3	e7a0bbb9-c26a-41e7-b9ee-60b0fcc139d4	0	性别未知	2026-04-14 23:31:02.199414	2026-04-14 23:31:02.199454
1	是	1		primary	t	sys_yes_no	2	4	db039e17-0f4c-4bc0-affe-a9ab22af3e28	0	是	2026-04-14 23:31:02.199464	2026-04-14 23:31:02.199465
2	否	0		danger	f	sys_yes_no	2	5	a0ed48df-9b73-42b8-b247-d1318199556c	0	否	2026-04-14 23:31:02.199469	2026-04-14 23:31:02.199469
1	启用	1		primary	f	sys_common_status	3	6	dbee6612-449c-4d82-9b15-e7f3be0513a3	0	启用状态	2026-04-14 23:31:02.199473	2026-04-14 23:31:02.199473
2	停用	0		danger	f	sys_common_status	3	7	38531061-ff79-4f5c-99f3-31a317fefe9f	0	停用状态	2026-04-14 23:31:02.199476	2026-04-14 23:31:02.199476
1	通知	1	blue	warning	t	sys_notice_type	4	8	06131532-3be9-4355-ba7c-3972f1c202f9	0	通知	2026-04-14 23:31:02.19948	2026-04-14 23:31:02.199481
2	公告	2	orange	success	f	sys_notice_type	4	9	1729653b-b1de-4369-9063-a6bb93010629	0	公告	2026-04-14 23:31:02.199484	2026-04-14 23:31:02.199484
99	其他	0		info	f	sys_oper_type	5	10	37f5045c-2311-40e5-8da9-e0e0be7119c8	0	其他操作	2026-04-14 23:31:02.199487	2026-04-14 23:31:02.199487
1	新增	1		info	f	sys_oper_type	5	11	af164d94-7cd4-43d4-8815-13bddcc15bb4	0	新增操作	2026-04-14 23:31:02.19949	2026-04-14 23:31:02.19949
2	修改	2		info	f	sys_oper_type	5	12	2d3c290c-ad23-45dc-a214-23de28229589	0	修改操作	2026-04-14 23:31:02.199493	2026-04-14 23:31:02.199493
3	删除	3		danger	f	sys_oper_type	5	13	9136603b-7a86-40f9-a2c0-e6f32455e1ab	0	删除操作	2026-04-14 23:31:02.199496	2026-04-14 23:31:02.199497
4	分配权限	4		primary	f	sys_oper_type	5	14	4640de47-f5af-4e8f-9d78-570a25b014df	0	授权操作	2026-04-14 23:31:02.1995	2026-04-14 23:31:02.1995
5	导出	5		warning	f	sys_oper_type	5	15	98fa0121-723d-4fb2-81ed-b6adddaf9554	0	导出操作	2026-04-14 23:31:02.199503	2026-04-14 23:31:02.199503
6	导入	6		warning	f	sys_oper_type	5	16	c957eded-b5f5-468f-ae8c-dbb04c7c7d2d	0	导入操作	2026-04-14 23:31:02.199506	2026-04-14 23:31:02.199506
7	强退	7		danger	f	sys_oper_type	5	17	2433414d-933f-459a-9062-d954455cf1b4	0	强退操作	2026-04-14 23:31:02.199509	2026-04-14 23:31:02.199509
8	生成代码	8		warning	f	sys_oper_type	5	18	3a2e099d-366b-454a-b761-e5648425b4bf	0	生成操作	2026-04-14 23:31:02.199512	2026-04-14 23:31:02.199513
9	清空数据	9		danger	f	sys_oper_type	5	19	399f9e01-ee35-4b20-9085-2e47625cac91	0	清空操作	2026-04-14 23:31:02.199515	2026-04-14 23:31:02.199516
1	默认(Memory)	default		\N	t	sys_job_store	6	20	d54ae708-3071-462f-a6d9-5d31733f6d89	0	默认分组	2026-04-14 23:31:02.199518	2026-04-14 23:31:02.199519
2	数据库(Sqlalchemy)	sqlalchemy		\N	f	sys_job_store	6	21	e7c09c06-6860-48b9-89ec-58ca4d96178a	0	数据库分组	2026-04-14 23:31:02.199521	2026-04-14 23:31:02.199522
3	数据库(Redis)	redis		\N	f	sys_job_store	6	22	9e327e08-13a5-46b3-9aa1-b7ed3b79dca4	0	reids分组	2026-04-14 23:31:02.199524	2026-04-14 23:31:02.199525
1	线程池	default		\N	f	sys_job_executor	7	23	3d0a7f42-2e1d-4630-b794-d7e5c7887764	0	线程池	2026-04-14 23:31:02.199528	2026-04-14 23:31:02.199528
2	进程池	processpool		\N	f	sys_job_executor	7	24	544a3a3b-2e74-4459-a292-8cb486eaa1c6	0	进程池	2026-04-14 23:31:02.199531	2026-04-14 23:31:02.199531
1	演示函数	scheduler_test.job		\N	t	sys_job_function	8	25	97714ca5-36c7-4efc-a522-062f01012c10	0	演示函数	2026-04-14 23:31:02.199534	2026-04-14 23:31:02.199534
1	指定日期(date)	date		\N	t	sys_job_trigger	9	26	d92505ac-7de0-4047-95ea-391706814a2c	0	指定日期任务触发器	2026-04-14 23:31:02.199537	2026-04-14 23:31:02.199537
2	间隔触发器(interval)	interval		\N	f	sys_job_trigger	9	27	8548b37a-ce40-46e5-9080-f3647868ae4b	0	间隔触发器任务触发器	2026-04-14 23:31:02.19954	2026-04-14 23:31:02.19954
3	cron表达式	cron		\N	f	sys_job_trigger	9	28	73391a0e-fc1f-481a-986a-0612b3291357	0	间隔触发器任务触发器	2026-04-14 23:31:02.199543	2026-04-14 23:31:02.199543
1	默认(default)	default		\N	t	sys_list_class	10	29	19da3591-c181-44e1-9f8c-c21293455a41	0	默认表格回显样式	2026-04-14 23:31:02.199546	2026-04-14 23:31:02.199546
2	主要(primary)	primary		\N	f	sys_list_class	10	30	29fc94d6-cda5-4817-9256-cc318cfc4122	0	主要表格回显样式	2026-04-14 23:31:02.199549	2026-04-14 23:31:02.199549
3	成功(success)	success		\N	f	sys_list_class	10	31	10d8b605-7c71-4189-93ee-be12d05b8ac9	0	成功表格回显样式	2026-04-14 23:31:02.199552	2026-04-14 23:31:02.199552
4	信息(info)	info		\N	f	sys_list_class	10	32	f2509a54-91f8-4ad0-97d7-d3edc8507961	0	信息表格回显样式	2026-04-14 23:31:02.199555	2026-04-14 23:31:02.199555
5	警告(warning)	warning		\N	f	sys_list_class	10	33	bfdee254-2e51-42e0-837c-53f76b36de59	0	警告表格回显样式	2026-04-14 23:31:02.199558	2026-04-14 23:31:02.199558
6	危险(danger)	danger		\N	f	sys_list_class	10	34	a355461b-11cf-4ccb-a537-3e5cdebaf89b	0	危险表格回显样式	2026-04-14 23:31:02.199561	2026-04-14 23:31:02.199561
\.


--
-- Data for Name: sys_dict_type; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_dict_type (dict_name, dict_type, id, uuid, status, description, created_time, updated_time) FROM stdin;
用户性别	sys_user_sex	1	0af908d5-be91-49a5-8c8c-1dd0ca6c3ac7	0	用户性别列表	2026-04-14 23:31:02.192484	2026-04-14 23:31:02.192485
系统是否	sys_yes_no	2	a10605af-905d-4d7b-a2dd-bb69c41a3d3b	0	系统是否列表	2026-04-14 23:31:02.192489	2026-04-14 23:31:02.192489
系统状态	sys_common_status	3	3e3c5f5e-373d-4557-b4f1-3f24caee4cf5	0	系统状态	2026-04-14 23:31:02.192493	2026-04-14 23:31:02.192493
通知类型	sys_notice_type	4	d258d54f-4daa-4e9e-96a9-0def2d7af833	0	通知类型列表	2026-04-14 23:31:02.192496	2026-04-14 23:31:02.192496
操作类型	sys_oper_type	5	df58139c-f559-441b-8805-f679859b9675	0	操作类型列表	2026-04-14 23:31:02.192499	2026-04-14 23:31:02.192499
任务存储器	sys_job_store	6	daf0d423-49ea-4af3-9fda-163490a2e67e	0	任务分组列表	2026-04-14 23:31:02.192502	2026-04-14 23:31:02.192502
任务执行器	sys_job_executor	7	0101339a-c18a-4869-b9f5-9efea2db8862	0	任务执行器列表	2026-04-14 23:31:02.192505	2026-04-14 23:31:02.192505
任务函数	sys_job_function	8	53b8bcb7-1a87-48b9-8ad6-ff9142ca50bb	0	任务函数列表	2026-04-14 23:31:02.192508	2026-04-14 23:31:02.192509
任务触发器	sys_job_trigger	9	2ae1adc5-14d7-4b2d-844c-3af7db76aa89	0	任务触发器列表	2026-04-14 23:31:02.192511	2026-04-14 23:31:02.192512
表格回显样式	sys_list_class	10	6c51f300-6ba4-4bdf-92d7-a2f17772f77b	0	表格回显样式列表	2026-04-14 23:31:02.192514	2026-04-14 23:31:02.192515
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
仪表盘	1	1		client	Dashboard	/dashboard	\N	/dashboard/workplace	f	t	t	仪表盘	null	f	\N	1	3c3ad5a4-cade-4d1b-af12-45ac6bcc35d7	0	初始化数据	2026-04-14 23:31:02.154425	2026-04-14 23:31:02.15443
系统管理	1	2	\N	system	System	/system	\N	/system/menu	f	t	f	系统管理	null	f	\N	2	91963258-7491-4c02-9c35-69ad63cff488	0	初始化数据	2026-04-14 23:31:02.154435	2026-04-14 23:31:02.154436
监控管理	1	3	\N	monitor	Monitor	/monitor	\N	/monitor/online	f	t	f	监控管理	null	f	\N	3	c76afed7-5412-4bbb-aaf2-16686269d1a4	0	初始化数据	2026-04-14 23:31:02.15444	2026-04-14 23:31:02.154441
接口管理	1	4	\N	document	Common	/common	\N	/common/docs	f	t	f	接口管理	null	f	\N	4	7da57c06-f7b6-4af8-8691-075151cc46ea	0	初始化数据	2026-04-14 23:31:02.154445	2026-04-14 23:31:02.154445
代码管理	1	5	\N	code	Generator	/generator	\N	/generator/gencode	f	t	f	代码管理	null	f	\N	5	277d2519-d684-409d-ab5c-780ceba9a4c1	0	代码管理	2026-04-14 23:31:02.154449	2026-04-14 23:31:02.154449
应用管理	1	6	\N	el-icon-ShoppingBag	Application	/application	\N	/application/portal	f	t	f	应用管理	null	f	\N	6	4896e08c-2542-46e8-9838-e8c645e95ed2	0	初始化数据	2026-04-14 23:31:02.154453	2026-04-14 23:31:02.154454
AI管理	1	7	\N	el-icon-ChatLineSquare	AI	/ai	\N	/ai/chat	f	t	f	AI管理	null	f	\N	7	fab5ff64-5bc0-4cc3-ac9e-c13d39496bb4	0	AI管理	2026-04-14 23:31:02.154458	2026-04-14 23:31:02.154458
任务管理	1	8	\N	el-icon-SetUp	Task	/task	\N	/task/cronjob/job	f	t	f	任务管理	null	f	\N	8	d9d8d114-956c-42b0-bba7-ea2f1411ff77	0	任务管理	2026-04-14 23:31:02.154462	2026-04-14 23:31:02.154462
案例管理	1	9	\N	menu	Example	/example	\N	/example/demo	f	t	f	案例管理	null	f	\N	9	5cf9f66d-3bb9-4c3f-aec1-bbe7264e7c58	0	案例管理	2026-04-14 23:31:02.154466	2026-04-14 23:31:02.154466
工作台	2	1	dashboard:workplace:query	el-icon-PieChart	Workplace	/dashboard/workplace	dashboard/workplace	\N	f	t	f	工作台	null	f	1	10	2ee2fc7f-0884-4537-ad92-f0fcfd5a9a22	0	初始化数据	2026-04-14 23:31:02.158355	2026-04-14 23:31:02.158358
菜单管理	2	1	module_system:menu:query	menu	Menu	/system/menu	module_system/menu/index	\N	f	t	f	菜单管理	null	f	2	11	ec0e5825-6005-45e7-bc58-6fae5c0819a2	0	初始化数据	2026-04-14 23:31:02.158361	2026-04-14 23:31:02.158362
部门管理	2	2	module_system:dept:query	tree	Dept	/system/dept	module_system/dept/index	\N	f	t	f	部门管理	null	f	2	12	e6aa5b19-a74b-4894-a6da-41aa3e6786de	0	初始化数据	2026-04-14 23:31:02.158365	2026-04-14 23:31:02.158366
岗位管理	2	3	module_system:position:query	el-icon-Coordinate	Position	/system/position	module_system/position/index	\N	f	t	f	岗位管理	null	f	2	13	5211a958-4904-4d0d-8092-274e7fe85c58	0	初始化数据	2026-04-14 23:31:02.158369	2026-04-14 23:31:02.158369
角色管理	2	4	module_system:role:query	role	Role	/system/role	module_system/role/index	\N	f	t	f	角色管理	null	f	2	14	6a8df465-cd58-4094-b27d-b8c56a139112	0	初始化数据	2026-04-14 23:31:02.158372	2026-04-14 23:31:02.158372
用户管理	2	5	module_system:user:query	el-icon-User	User	/system/user	module_system/user/index	\N	f	t	f	用户管理	null	f	2	15	7ce5f779-6a42-49a4-af73-9a898b8d6561	0	初始化数据	2026-04-14 23:31:02.158375	2026-04-14 23:31:02.158376
日志管理	2	6	module_system:log:query	el-icon-Aim	Log	/system/log	module_system/log/index	\N	f	t	f	日志管理	null	f	2	16	1c7dc70f-d51d-48ff-afb3-c87732bdd0e8	0	初始化数据	2026-04-14 23:31:02.158379	2026-04-14 23:31:02.158379
公告管理	2	7	module_system:notice:query	bell	Notice	/system/notice	module_system/notice/index	\N	f	t	f	公告管理	null	f	2	17	47f8170b-6789-4b59-9873-e8860313a5aa	0	初始化数据	2026-04-14 23:31:02.158382	2026-04-14 23:31:02.158383
参数管理	2	8	module_system:param:query	setting	Params	/system/param	module_system/param/index	\N	f	t	f	参数管理	null	f	2	18	c515a603-3d39-401d-8b9d-339ce7bd31a1	0	初始化数据	2026-04-14 23:31:02.158385	2026-04-14 23:31:02.158386
字典管理	2	9	module_system:dict_type:query	dict	Dict	/system/dict	module_system/dict/index	\N	f	t	f	字典管理	null	f	2	19	dab16bb4-96fa-4320-b997-5f693348fcfe	0	初始化数据	2026-04-14 23:31:02.158389	2026-04-14 23:31:02.158389
租户管理	2	10	module_system:tenant:query	el-icon-DataBoard	Tenant	/system/tenant	module_system/tenant/index	\N	f	t	f	租户管理	null	f	2	20	79fed437-908b-4f3a-a1c3-100d1c408d46	0	初始化数据	2026-04-14 23:31:02.158392	2026-04-14 23:31:02.158393
在线用户	2	1	module_monitor:online:query	el-icon-Headset	MonitorOnline	/monitor/online	module_monitor/online/index	\N	f	t	f	在线用户	null	f	3	21	ecc8a396-521d-462b-abb8-1863a3454e6d	0	初始化数据	2026-04-14 23:31:02.158396	2026-04-14 23:31:02.158396
服务器监控	2	2	module_monitor:server:query	el-icon-Odometer	MonitorServer	/monitor/server	module_monitor/server/index	\N	f	t	f	服务器监控	null	f	3	22	82189917-d398-4a2f-80a8-dc507cbf0ee2	0	初始化数据	2026-04-14 23:31:02.158399	2026-04-14 23:31:02.158399
缓存监控	2	3	module_monitor:cache:query	el-icon-Stopwatch	MonitorCache	/monitor/cache	module_monitor/cache/index	\N	f	t	f	缓存监控	null	f	3	23	a9bb4de2-e666-4cf3-9f7a-2ce55759b3b5	0	初始化数据	2026-04-14 23:31:02.158402	2026-04-14 23:31:02.158402
文件管理	2	4	module_monitor:resource:query	el-icon-Files	Resource	/monitor/resource	module_monitor/resource/index	\N	f	t	f	文件管理	null	f	3	24	ac9f25d1-24a5-44fb-958b-9e025497ef18	0	初始化数据	2026-04-14 23:31:02.158405	2026-04-14 23:31:02.158406
Swagger文档	4	1	module_common:docs:query	api	Docs	/common/docs	module_common/docs/index	\N	f	t	f	Swagger文档	null	f	4	25	642439f3-a53d-414b-8aab-eb6546973089	0	初始化数据	2026-04-14 23:31:02.158409	2026-04-14 23:31:02.158409
Redoc文档	4	2	module_common:redoc:query	el-icon-Document	Redoc	/common/redoc	module_common/redoc/index	\N	f	t	f	Redoc文档	null	f	4	26	95a6cb4c-87d5-449f-825f-719588017ffc	0	初始化数据	2026-04-14 23:31:02.158412	2026-04-14 23:31:02.158412
LangJin文档	4	3	module_common:ljdoc:query	el-icon-Document	Ljdoc	/common/ljdoc	module_common/ljdoc/index	\N	f	t	f	LangJin文档	null	f	4	27	aaa17960-095d-4cd1-9ae9-54b9a65b793d	0	初始化数据	2026-04-14 23:31:02.158415	2026-04-14 23:31:02.158415
代码生成	2	1	module_generator:gencode:query	code	GenCode	/generator/gencode	module_generator/gencode/index	\N	f	t	f	代码生成	null	f	5	28	8815a286-e25b-4e9b-9100-579a82173edf	0	代码生成	2026-04-14 23:31:02.158418	2026-04-14 23:31:02.158418
插件市场	2	1	module_application:portal:query	el-icon-ShoppingCartFull	PortalApp	/application/portal	module_application/portal/index	\N	f	t	f	插件市场	null	f	6	29	bdc0370b-7a4b-497f-851e-3c248d3e5882	0	初始化数据	2026-04-14 23:31:02.158421	2026-04-14 23:31:02.158421
AI智能助手	2	1	module_ai:chat:query	el-icon-ChatDotRound	Chat	/ai/chat	module_ai/chat/index	\N	f	t	f	AI智能助手	null	f	7	30	d2f10273-657f-43a1-886d-eecf7c260110	0	AI智能助手	2026-04-14 23:31:02.158424	2026-04-14 23:31:02.158425
会话记忆	2	2	module_ai:chat:query	el-icon-ChatLineSquare	Memory	/ai/memory	module_ai/memory/index	\N	f	t	f	会话记忆	null	f	7	31	96ba409e-8671-4878-99b1-f64e5525be7e	0	会话记忆管理	2026-04-14 23:31:02.158428	2026-04-14 23:31:02.158428
定时任务	1	1	\N	el-icon-Timer	Cronjob	/task/cronjob	\N	/task/cronjob/job	f	t	t	定时任务	null	f	8	32	a6702091-d49e-4582-bfb5-8709924607b7	0	APScheduler 调度器与任务节点	2026-04-14 23:31:02.158431	2026-04-14 23:31:02.158431
工作流	1	2	\N	el-icon-SetUp	WorkflowMgr	/task/workflow-mgr	\N	/task/workflow/definition	f	t	t	工作流	null	f	8	33	459e17f2-b54c-4726-acb7-2bf1c7887d76	0	流程编排与编排节点类型	2026-04-14 23:31:02.158434	2026-04-14 23:31:02.158434
示例管理	2	1	module_example:demo:query	menu	Demo	/example/demo	module_example/demo/index	\N	f	t	f	示例管理	null	f	9	34	2a823154-1402-46fb-9d07-45b42aa7df86	0	示例管理	2026-04-14 23:31:02.158437	2026-04-14 23:31:02.158437
二级目录	1	2	\N	menu	DemoDir	/example/demo-group	\N	/example/demo-group/demo01	f	t	t	二级目录	null	f	9	35	81fd396d-6f3c-487b-9d70-0e6a71bb34de	0	二级目录（含三级菜单）	2026-04-14 23:31:02.158441	2026-04-14 23:31:02.158441
创建菜单	3	1	module_system:menu:create	\N	\N	\N	\N	\N	f	t	f	创建菜单	null	f	11	36	540fc2d2-cb15-4170-838e-08880ba2faa8	0	初始化数据	2026-04-14 23:31:02.16421	2026-04-14 23:31:02.164213
修改菜单	3	2	module_system:menu:update	\N	\N	\N	\N	\N	f	t	f	修改菜单	null	f	11	37	0e60a5ab-af83-47b0-b28d-0db75cbc2f75	0	初始化数据	2026-04-14 23:31:02.164218	2026-04-14 23:31:02.164219
删除菜单	3	3	module_system:menu:delete	\N	\N	\N	\N	\N	f	t	f	删除菜单	null	f	11	38	89912574-845d-4bd7-b694-36d5ba6cd1c5	0	初始化数据	2026-04-14 23:31:02.164222	2026-04-14 23:31:02.164223
批量修改菜单状态	3	4	module_system:menu:patch	\N	\N	\N	\N	\N	f	t	f	批量修改菜单状态	null	f	11	39	37122605-fc5a-49d0-a4e0-01217c520b24	0	初始化数据	2026-04-14 23:31:02.164226	2026-04-14 23:31:02.164226
详情菜单	3	5	module_system:menu:detail	\N	\N	\N	\N	\N	f	t	f	详情菜单	null	f	11	40	7d28935d-dac5-44a2-ab4b-1e6d6a0db30b	0	初始化数据	2026-04-14 23:31:02.164229	2026-04-14 23:31:02.164229
查询菜单	3	6	module_system:menu:query	\N	\N	\N	\N	\N	f	t	f	查询菜单	null	f	11	41	acb35b70-1a9f-4d5e-81a1-ddf9d40764f1	0	初始化数据	2026-04-14 23:31:02.164232	2026-04-14 23:31:02.164232
创建部门	3	1	module_system:dept:create	\N	\N	\N	\N	\N	f	t	f	创建部门	null	f	12	42	df361b1b-8efe-4c3f-92f4-40f8b260df1d	0	初始化数据	2026-04-14 23:31:02.164235	2026-04-14 23:31:02.164236
修改部门	3	2	module_system:dept:update	\N	\N	\N	\N	\N	f	t	f	修改部门	null	f	12	43	b495e752-a4bb-4b39-b4e9-14fa663cf31a	0	初始化数据	2026-04-14 23:31:02.164238	2026-04-14 23:31:02.164239
删除部门	3	3	module_system:dept:delete	\N	\N	\N	\N	\N	f	t	f	删除部门	null	f	12	44	ece480dc-af81-409b-ab97-b4e5c5f8d302	0	初始化数据	2026-04-14 23:31:02.164242	2026-04-14 23:31:02.164242
批量修改部门状态	3	4	module_system:dept:patch	\N	\N	\N	\N	\N	f	t	f	批量修改部门状态	null	f	12	45	27ed7565-56e0-414d-a194-88c6e60bf5a5	0	初始化数据	2026-04-14 23:31:02.164245	2026-04-14 23:31:02.164245
详情部门	3	5	module_system:dept:detail	\N	\N	\N	\N	\N	f	t	f	详情部门	null	f	12	46	f5f898c4-7f6f-40ff-8816-0559761090f0	0	初始化数据	2026-04-14 23:31:02.164248	2026-04-14 23:31:02.164248
查询部门	3	6	module_system:dept:query	\N	\N	\N	\N	\N	f	t	f	查询部门	null	f	12	47	30e919fe-f7fc-47fa-97dc-f2a1cc81037c	0	初始化数据	2026-04-14 23:31:02.164251	2026-04-14 23:31:02.164251
创建岗位	3	1	module_system:position:create	\N	\N	\N	\N	\N	f	t	f	创建岗位	null	f	13	48	514a4d52-1139-4510-b1fa-6dcb5f252277	0	初始化数据	2026-04-14 23:31:02.164254	2026-04-14 23:31:02.164255
修改岗位	3	2	module_system:position:update	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	13	49	9b312182-7d32-4926-986e-67033963ca6f	0	初始化数据	2026-04-14 23:31:02.164257	2026-04-14 23:31:02.164258
删除岗位	3	3	module_system:position:delete	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	13	50	f84f2cdb-2075-405d-8155-053fed8fd3dc	0	初始化数据	2026-04-14 23:31:02.164261	2026-04-14 23:31:02.164261
批量修改岗位状态	3	4	module_system:position:patch	\N	\N	\N	\N	\N	f	t	f	批量修改岗位状态	null	f	13	51	39107bb5-d828-4a6e-a8c6-0a85b86f7a4c	0	初始化数据	2026-04-14 23:31:02.164264	2026-04-14 23:31:02.164264
岗位导出	3	5	module_system:position:export	\N	\N	\N	\N	\N	f	t	f	岗位导出	null	f	13	52	0ff07589-197d-433b-9956-909aee0d9da7	0	初始化数据	2026-04-14 23:31:02.164267	2026-04-14 23:31:02.164267
详情岗位	3	6	module_system:position:detail	\N	\N	\N	\N	\N	f	t	f	详情岗位	null	f	13	53	ed35406a-1aad-4000-9a66-a37a8ced3363	0	初始化数据	2026-04-14 23:31:02.16427	2026-04-14 23:31:02.164271
查询岗位	3	7	module_system:position:query	\N	\N	\N	\N	\N	f	t	f	查询岗位	null	f	13	54	2cb47576-f953-46a8-86cc-cf54a5de2bbe	0	初始化数据	2026-04-14 23:31:02.164273	2026-04-14 23:31:02.164274
创建角色	3	1	module_system:role:create	\N	\N	\N	\N	\N	f	t	f	创建角色	null	f	14	55	4f8a4535-53ce-474b-b188-71d832dd6092	0	初始化数据	2026-04-14 23:31:02.164277	2026-04-14 23:31:02.164277
修改角色	3	2	module_system:role:update	\N	\N	\N	\N	\N	f	t	f	修改角色	null	f	14	56	8118efa1-a65c-4b2d-ba4b-b99bf612947f	0	初始化数据	2026-04-14 23:31:02.16428	2026-04-14 23:31:02.16428
删除角色	3	3	module_system:role:delete	\N	\N	\N	\N	\N	f	t	f	删除角色	null	f	14	57	9b27d713-090a-45cd-af61-ae6e62a0f7e7	0	初始化数据	2026-04-14 23:31:02.164283	2026-04-14 23:31:02.164283
批量修改角色状态	3	4	module_system:role:patch	\N	\N	\N	\N	\N	f	t	f	批量修改角色状态	null	f	14	58	20fbcac8-6f1f-482c-8026-836d03c802e6	0	初始化数据	2026-04-14 23:31:02.164286	2026-04-14 23:31:02.164286
角色导出	3	5	module_system:role:export	\N	\N	\N	\N	\N	f	t	f	角色导出	null	f	14	59	9b0d4c12-fa65-4d19-964a-179506918bac	0	初始化数据	2026-04-14 23:31:02.164289	2026-04-14 23:31:02.16429
详情角色	3	6	module_system:role:detail	\N	\N	\N	\N	\N	f	t	f	详情角色	null	f	14	60	40789ef4-0541-4dc6-afaf-83a2168e109a	0	初始化数据	2026-04-14 23:31:02.164292	2026-04-14 23:31:02.164293
查询角色	3	7	module_system:role:query	\N	\N	\N	\N	\N	f	t	f	查询角色	null	f	14	61	0f533204-1c2d-4671-9ca8-faa51d9cc6c8	0	初始化数据	2026-04-14 23:31:02.164295	2026-04-14 23:31:02.164296
分配权限	3	8	module_system:role:permission	\N	\N	\N	\N	\N	f	t	f	分配权限	null	f	14	62	c1a88b4c-279a-442d-b3d8-3b79a9ccb587	0	初始化数据	2026-04-14 23:31:02.164299	2026-04-14 23:31:02.164299
创建用户	3	1	module_system:user:create	\N	\N	\N	\N	\N	f	t	f	创建用户	null	f	15	63	8ee512c1-67b3-45af-b58e-13940359b623	0	初始化数据	2026-04-14 23:31:02.164302	2026-04-14 23:31:02.164302
修改用户	3	2	module_system:user:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	15	64	910eaa9c-9502-4844-8589-2b4288d0ebe1	0	初始化数据	2026-04-14 23:31:02.164305	2026-04-14 23:31:02.164305
删除用户	3	3	module_system:user:delete	\N	\N	\N	\N	\N	f	t	f	删除用户	null	f	15	65	9283fe29-e731-40e5-a668-0f5c63b0029c	0	初始化数据	2026-04-14 23:31:02.164308	2026-04-14 23:31:02.164308
批量修改用户状态	3	4	module_system:user:patch	\N	\N	\N	\N	\N	f	t	f	批量修改用户状态	null	f	15	66	090a38b6-473b-491b-adaf-04b0310dcb35	0	初始化数据	2026-04-14 23:31:02.164311	2026-04-14 23:31:02.164311
导出用户	3	5	module_system:user:export	\N	\N	\N	\N	\N	f	t	f	导出用户	null	f	15	67	f8d2cbe5-d117-4ef4-a027-a61b6de51e2a	0	初始化数据	2026-04-14 23:31:02.164314	2026-04-14 23:31:02.164314
导入用户	3	6	module_system:user:import	\N	\N	\N	\N	\N	f	t	f	导入用户	null	f	15	68	6705934f-e689-4fe5-bdde-d258103b0e2e	0	初始化数据	2026-04-14 23:31:02.164317	2026-04-14 23:31:02.164318
下载用户导入模板	3	7	module_system:user:download	\N	\N	\N	\N	\N	f	t	f	下载用户导入模板	null	f	15	69	1bd9949d-ca22-438a-9464-a320d90a675c	0	初始化数据	2026-04-14 23:31:02.16432	2026-04-14 23:31:02.164321
详情用户	3	8	module_system:user:detail	\N	\N	\N	\N	\N	f	t	f	详情用户	null	f	15	70	13f4b60f-3b1e-459a-a76a-5cf8da531892	0	初始化数据	2026-04-14 23:31:02.164323	2026-04-14 23:31:02.164324
查询用户	3	9	module_system:user:query	\N	\N	\N	\N	\N	f	t	f	查询用户	null	f	15	71	41fa2b34-8099-4d7b-bca5-06286e9c3a2e	0	初始化数据	2026-04-14 23:31:02.164326	2026-04-14 23:31:02.164327
日志删除	3	1	module_system:log:delete	\N	\N	\N	\N	\N	f	t	f	日志删除	null	f	16	72	61b6fb26-7321-4ebd-9686-96d027b50c9d	0	初始化数据	2026-04-14 23:31:02.164332	2026-04-14 23:31:02.164333
日志导出	3	2	module_system:log:export	\N	\N	\N	\N	\N	f	t	f	日志导出	null	f	16	73	8f8fd135-5a88-40a9-ba73-86616f9fe872	0	初始化数据	2026-04-14 23:31:02.164336	2026-04-14 23:31:02.164337
日志详情	3	3	module_system:log:detail	\N	\N	\N	\N	\N	f	t	f	日志详情	null	f	16	74	2fab50d2-e7c5-4032-87d0-1560265306f8	0	初始化数据	2026-04-14 23:31:02.164339	2026-04-14 23:31:02.16434
查询日志	3	4	module_system:log:query	\N	\N	\N	\N	\N	f	t	f	查询日志	null	f	16	75	fe491791-aafa-4535-bbec-bd0a0e888250	0	初始化数据	2026-04-14 23:31:02.164342	2026-04-14 23:31:02.164343
公告创建	3	1	module_system:notice:create	\N	\N	\N	\N	\N	f	t	f	公告创建	null	f	17	76	29476ea2-5a29-4cd4-9a12-664927a01980	0	初始化数据	2026-04-14 23:31:02.164346	2026-04-14 23:31:02.164346
公告修改	3	2	module_system:notice:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	17	77	d749420d-93bf-4bb3-8f8a-5f4450f43b40	0	初始化数据	2026-04-14 23:31:02.164349	2026-04-14 23:31:02.164349
公告删除	3	3	module_system:notice:delete	\N	\N	\N	\N	\N	f	t	f	公告删除	null	f	17	78	473966c2-039d-4580-ae03-1be48302569b	0	初始化数据	2026-04-14 23:31:02.164352	2026-04-14 23:31:02.164352
公告导出	3	4	module_system:notice:export	\N	\N	\N	\N	\N	f	t	f	公告导出	null	f	17	79	ae5fcb79-b969-461a-9567-7434aebbf18d	0	初始化数据	2026-04-14 23:31:02.164355	2026-04-14 23:31:02.164355
公告批量修改状态	3	5	module_system:notice:patch	\N	\N	\N	\N	\N	f	t	f	公告批量修改状态	null	f	17	80	99c03607-7ca3-487b-8491-49e2f0e9d26b	0	初始化数据	2026-04-14 23:31:02.164358	2026-04-14 23:31:02.164358
公告详情	3	6	module_system:notice:detail	\N	\N	\N	\N	\N	f	t	f	公告详情	null	f	17	81	7414f660-800f-4280-b90a-bbe54625458b	0	初始化数据	2026-04-14 23:31:02.164361	2026-04-14 23:31:02.164362
查询公告	3	5	module_system:notice:query	\N	\N	\N	\N	\N	f	t	f	查询公告	null	f	17	82	4a1d7d78-bdd7-4dbf-b029-c0d89bff25c9	0	初始化数据	2026-04-14 23:31:02.164364	2026-04-14 23:31:02.164365
创建参数	3	1	module_system:param:create	\N	\N	\N	\N	\N	f	t	f	创建参数	null	f	18	83	ce47df31-5427-4326-b189-5d4d67bca775	0	初始化数据	2026-04-14 23:31:02.164367	2026-04-14 23:31:02.164368
修改参数	3	2	module_system:param:update	\N	\N	\N	\N	\N	f	t	f	修改参数	null	f	18	84	a72972f9-5454-4b74-9ae1-5b2f1f51aac3	0	初始化数据	2026-04-14 23:31:02.16437	2026-04-14 23:31:02.164371
删除参数	3	3	module_system:param:delete	\N	\N	\N	\N	\N	f	t	f	删除参数	null	f	18	85	5a8036e0-e07a-4c84-9044-671084c2b483	0	初始化数据	2026-04-14 23:31:02.164374	2026-04-14 23:31:02.164374
导出参数	3	4	module_system:param:export	\N	\N	\N	\N	\N	f	t	f	导出参数	null	f	18	86	565df445-3c9a-4dae-8dda-e49ffe4a79a9	0	初始化数据	2026-04-14 23:31:02.164377	2026-04-14 23:31:02.164377
参数上传	3	5	module_system:param:upload	\N	\N	\N	\N	\N	f	t	f	参数上传	null	f	18	87	81ba0d6e-cb54-4163-bce5-2be61db9aeff	0	初始化数据	2026-04-14 23:31:02.16438	2026-04-14 23:31:02.16438
参数详情	3	6	module_system:param:detail	\N	\N	\N	\N	\N	f	t	f	参数详情	null	f	18	88	19d78dd0-52ca-4231-8265-5711afa40359	0	初始化数据	2026-04-14 23:31:02.164383	2026-04-14 23:31:02.164383
查询参数	3	7	module_system:param:query	\N	\N	\N	\N	\N	f	t	f	查询参数	null	f	18	89	0b2e23f8-676e-4159-8e18-1eb66c5d36cb	0	初始化数据	2026-04-14 23:31:02.164386	2026-04-14 23:31:02.164386
创建字典类型	3	1	module_system:dict_type:create	\N	\N	\N	\N	\N	f	t	f	创建字典类型	null	f	19	90	42053096-4694-4374-b5c8-254800ba02b6	0	初始化数据	2026-04-14 23:31:02.164389	2026-04-14 23:31:02.16439
修改字典类型	3	2	module_system:dict_type:update	\N	\N	\N	\N	\N	f	t	f	修改字典类型	null	f	19	91	bd7f4aed-c31d-4563-8ef5-85707b69026d	0	初始化数据	2026-04-14 23:31:02.164392	2026-04-14 23:31:02.164393
删除字典类型	3	3	module_system:dict_type:delete	\N	\N	\N	\N	\N	f	t	f	删除字典类型	null	f	19	92	49d010b8-e5c2-4a1f-9b2e-be53208be4ff	0	初始化数据	2026-04-14 23:31:02.164395	2026-04-14 23:31:02.164396
导出字典类型	3	4	module_system:dict_type:export	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	19	93	4a92fe73-8f42-4ad9-8ab1-d2be64a98d0e	0	初始化数据	2026-04-14 23:31:02.164398	2026-04-14 23:31:02.164399
批量修改字典状态	3	5	module_system:dict_type:patch	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	19	94	60522346-732d-4d5c-9c85-5bbebe107f21	0	初始化数据	2026-04-14 23:31:02.164402	2026-04-14 23:31:02.164402
字典数据查询	3	6	module_system:dict_data:query	\N	\N	\N	\N	\N	f	t	f	字典数据查询	null	f	19	95	8a7f5157-c2d6-4f77-9564-552ed96f25ae	0	初始化数据	2026-04-14 23:31:02.164405	2026-04-14 23:31:02.164405
创建字典数据	3	7	module_system:dict_data:create	\N	\N	\N	\N	\N	f	t	f	创建字典数据	null	f	19	96	d772486d-a481-45ef-a95b-563c1bd54ffa	0	初始化数据	2026-04-14 23:31:02.164408	2026-04-14 23:31:02.164408
修改字典数据	3	8	module_system:dict_data:update	\N	\N	\N	\N	\N	f	t	f	修改字典数据	null	f	19	97	33c5a5dd-8fe0-416c-b9c5-60c6f31f083d	0	初始化数据	2026-04-14 23:31:02.164411	2026-04-14 23:31:02.164411
删除字典数据	3	9	module_system:dict_data:delete	\N	\N	\N	\N	\N	f	t	f	删除字典数据	null	f	19	98	8a5de749-55b0-4bd4-bf3c-4ea96d0997a0	0	初始化数据	2026-04-14 23:31:02.164414	2026-04-14 23:31:02.164414
导出字典数据	3	10	module_system:dict_data:export	\N	\N	\N	\N	\N	f	t	f	导出字典数据	null	f	19	99	e5756b94-1f23-49d4-9236-fe4b14edbf65	0	初始化数据	2026-04-14 23:31:02.164417	2026-04-14 23:31:02.164417
批量修改字典数据状态	3	11	module_system:dict_data:patch	\N	\N	\N	\N	\N	f	t	f	批量修改字典数据状态	null	f	19	100	c76ed045-03af-471f-8f40-e19041f9ea9b	0	初始化数据	2026-04-14 23:31:02.16442	2026-04-14 23:31:02.164421
详情字典类型	3	12	module_system:dict_type:detail	\N	\N	\N	\N	\N	f	t	f	详情字典类型	null	f	19	101	81fb6cf9-8906-499c-b984-b1c080fbb893	0	初始化数据	2026-04-14 23:31:02.164423	2026-04-14 23:31:02.164424
查询字典类型	3	13	module_system:dict_type:query	\N	\N	\N	\N	\N	f	t	f	查询字典类型	null	f	19	102	d7124675-47b6-435f-9ff0-ff7b7f0c08ad	0	初始化数据	2026-04-14 23:31:02.164426	2026-04-14 23:31:02.164427
详情字典数据	3	14	module_system:dict_data:detail	\N	\N	\N	\N	\N	f	t	f	详情字典数据	null	f	19	103	39190b00-db21-4178-9ba7-a620b8a11f54	0	初始化数据	2026-04-14 23:31:02.16443	2026-04-14 23:31:02.16443
创建租户	3	1	module_system:tenant:create	\N	\N	\N	\N	\N	f	t	f	创建租户	null	f	20	104	cfed9594-2f71-489a-971c-fb7ab308f1c9	0	初始化数据	2026-04-14 23:31:02.164433	2026-04-14 23:31:02.164433
修改租户	3	2	module_system:tenant:update	\N	\N	\N	\N	\N	f	t	f	修改租户	null	f	20	105	df11b27c-de7c-4324-bc85-e8e01ad388ff	0	初始化数据	2026-04-14 23:31:02.164436	2026-04-14 23:31:02.164436
删除租户	3	3	module_system:tenant:delete	\N	\N	\N	\N	\N	f	t	f	删除租户	null	f	20	106	d8b65ead-827a-4211-8ded-50c07ec45d95	0	初始化数据	2026-04-14 23:31:02.164439	2026-04-14 23:31:02.164439
批量修改租户状态	3	4	module_system:tenant:patch	\N	\N	\N	\N	\N	f	t	f	批量修改租户状态	null	f	20	107	3e4ed22f-fb35-4d5c-8b1c-6ef22a6f9903	0	初始化数据	2026-04-14 23:31:02.164442	2026-04-14 23:31:02.164442
租户详情	3	5	module_system:tenant:query	\N	\N	\N	\N	\N	f	t	f	租户详情	null	f	20	108	1cd70de7-da8d-4b83-b546-fa69377cfabf	0	初始化数据	2026-04-14 23:31:02.164445	2026-04-14 23:31:02.164446
查询租户	3	6	module_system:tenant:query	\N	\N	\N	\N	\N	f	t	f	查询租户	null	f	20	109	09b76692-2cb0-4cd5-8d61-3b723bca1dd2	0	初始化数据	2026-04-14 23:31:02.164448	2026-04-14 23:31:02.164449
在线用户强制下线	3	1	module_monitor:online:delete	\N	\N	\N	\N	\N	f	t	f	在线用户强制下线	null	f	21	110	8c9d6401-cc89-4878-85bf-b4ff707ad030	0	初始化数据	2026-04-14 23:31:02.164452	2026-04-14 23:31:02.164452
清除缓存	3	1	module_monitor:cache:delete	\N	\N	\N	\N	\N	f	t	f	清除缓存	null	f	23	111	f45558d6-8277-4d60-bb87-55c194cbb6a9	0	初始化数据	2026-04-14 23:31:02.164455	2026-04-14 23:31:02.164455
文件上传	3	1	module_monitor:resource:upload	\N	\N	\N	\N	\N	f	t	f	文件上传	null	f	24	112	cd487c5a-ab8f-459a-82eb-1a1461704088	0	初始化数据	2026-04-14 23:31:02.164458	2026-04-14 23:31:02.164458
文件下载	3	2	module_monitor:resource:download	\N	\N	\N	\N	\N	f	t	f	文件下载	null	f	24	113	3be7e8b7-4507-477f-876f-bb3d36a55b6d	0	初始化数据	2026-04-14 23:31:02.164461	2026-04-14 23:31:02.164461
文件删除	3	3	module_monitor:resource:delete	\N	\N	\N	\N	\N	f	t	f	文件删除	null	f	24	114	dd6aa035-e376-471b-845b-93982e61a405	0	初始化数据	2026-04-14 23:31:02.164464	2026-04-14 23:31:02.164464
文件移动	3	4	module_monitor:resource:move	\N	\N	\N	\N	\N	f	t	f	文件移动	null	f	24	115	5c9a8587-23ba-4887-af0c-a1de18d345b7	0	初始化数据	2026-04-14 23:31:02.164467	2026-04-14 23:31:02.164467
文件复制	3	5	module_monitor:resource:copy	\N	\N	\N	\N	\N	f	t	f	文件复制	null	f	24	116	1dec3f92-66cd-4ac9-8027-b47fd7c0fbdc	0	初始化数据	2026-04-14 23:31:02.16447	2026-04-14 23:31:02.164471
文件重命名	3	6	module_monitor:resource:rename	\N	\N	\N	\N	\N	f	t	f	文件重命名	null	f	24	117	cad65a3b-5080-448a-9cf0-c476bf2c61b8	0	初始化数据	2026-04-14 23:31:02.164473	2026-04-14 23:31:02.164474
创建目录	3	7	module_monitor:resource:create_dir	\N	\N	\N	\N	\N	f	t	f	创建目录	null	f	24	118	f204315c-a033-410e-a23f-47b587151e23	0	初始化数据	2026-04-14 23:31:02.164476	2026-04-14 23:31:02.164477
导出文件列表	3	9	module_monitor:resource:export	\N	\N	\N	\N	\N	f	t	f	导出文件列表	null	f	24	119	3cb08172-1897-4c98-8dc6-c2078bd89926	0	初始化数据	2026-04-14 23:31:02.164479	2026-04-14 23:31:02.16448
查询代码生成业务表列表	3	1	module_generator:gencode:query	\N	\N	\N	\N	\N	f	t	f	查询代码生成业务表列表	null	f	28	120	3011af64-2357-44cd-996c-06c0065d8a91	0	查询代码生成业务表列表	2026-04-14 23:31:02.164483	2026-04-14 23:31:02.164483
创建表结构	3	2	module_generator:gencode:create	\N	\N	\N	\N	\N	f	t	f	创建表结构	null	f	28	121	78e90f6c-5e00-4585-af01-1b6eac0d6a67	0	创建表结构	2026-04-14 23:31:02.164486	2026-04-14 23:31:02.164486
编辑业务表信息	3	3	module_generator:gencode:update	\N	\N	\N	\N	\N	f	t	f	编辑业务表信息	null	f	28	122	b09f3297-9e70-4a66-ac0b-836120b706bf	0	编辑业务表信息	2026-04-14 23:31:02.164489	2026-04-14 23:31:02.164489
删除业务表信息	3	4	module_generator:gencode:delete	\N	\N	\N	\N	\N	f	t	f	删除业务表信息	null	f	28	123	6c5c8b6e-9423-4307-8ee6-5673058c351f	0	删除业务表信息	2026-04-14 23:31:02.164492	2026-04-14 23:31:02.164492
导入表结构	3	5	module_generator:gencode:import	\N	\N	\N	\N	\N	f	t	f	导入表结构	null	f	28	124	9b61de5a-1492-4a95-8edd-0cb79d639093	0	导入表结构	2026-04-14 23:31:02.164495	2026-04-14 23:31:02.164495
批量生成代码	3	6	module_generator:gencode:operate	\N	\N	\N	\N	\N	f	t	f	批量生成代码	null	f	28	125	d307a89f-9068-4fa6-bc2d-d8f7899fcaff	0	批量生成代码	2026-04-14 23:31:02.164498	2026-04-14 23:31:02.164498
生成代码到指定路径	3	7	module_generator:gencode:code	\N	\N	\N	\N	\N	f	t	f	生成代码到指定路径	null	f	28	126	d3e38215-1350-48bc-9b6b-24c369bc4d3a	0	生成代码到指定路径	2026-04-14 23:31:02.164501	2026-04-14 23:31:02.164501
查询数据库表列表	3	8	module_generator:dblist:query	\N	\N	\N	\N	\N	f	t	f	查询数据库表列表	null	f	28	127	e05a97ff-6de6-4627-8bca-6d067896c67c	0	查询数据库表列表	2026-04-14 23:31:02.164504	2026-04-14 23:31:02.164505
同步数据库	3	9	module_generator:db:sync	\N	\N	\N	\N	\N	f	t	f	同步数据库	null	f	28	128	89cd66d0-b9d4-4a9d-ae5d-410ecf51144a	0	同步数据库	2026-04-14 23:31:02.164507	2026-04-14 23:31:02.164508
创建插件	3	1	module_application:portal:create	\N	\N	\N	\N	\N	f	t	f	创建插件	null	f	29	129	ec7ee4c6-5fcd-4988-b8c8-581c10db34d6	0	初始化数据	2026-04-14 23:31:02.16451	2026-04-14 23:31:02.164511
修改插件	3	2	module_application:portal:update	\N	\N	\N	\N	\N	f	t	f	修改插件	null	f	29	130	1b71fb0c-0866-4fae-93fa-ee396bcd9489	0	初始化数据	2026-04-14 23:31:02.164513	2026-04-14 23:31:02.164514
删除插件	3	3	module_application:portal:delete	\N	\N	\N	\N	\N	f	t	f	删除插件	null	f	29	131	5955f82b-425c-4313-9c6b-ffb817f231e3	0	初始化数据	2026-04-14 23:31:02.164517	2026-04-14 23:31:02.164517
批量修改插件状态	3	4	module_application:portal:patch	\N	\N	\N	\N	\N	f	t	f	批量修改应用状态	null	f	29	132	061e4025-0b69-4b99-ac55-7c6698c1755a	0	初始化数据	2026-04-14 23:31:02.16452	2026-04-14 23:31:02.16452
详情插件	3	5	module_application:portal:detail	\N	\N	\N	\N	\N	f	t	f	详情插件	null	f	29	133	6f04677f-43c1-4bba-b9a9-7e01d800af3e	0	初始化数据	2026-04-14 23:31:02.164523	2026-04-14 23:31:02.164523
查询插件	3	6	module_application:portal:query	\N	\N	\N	\N	\N	f	t	f	查询插件	null	f	29	134	1ad9ce56-acfa-4a8f-87cd-361ab1ccd1cb	0	查询插件	2026-04-14 23:31:02.164526	2026-04-14 23:31:02.164526
AI对话	3	1	module_ai:chat:ws	\N	\N	\N	\N	\N	f	t	f	AI对话	null	f	30	135	07961a38-db3a-416c-b456-c8b249e125b7	0	AI对话	2026-04-14 23:31:02.164529	2026-04-14 23:31:02.16453
查询会话	3	2	module_ai:chat:query	\N	\N	\N	\N	\N	f	t	f	查询会话	null	f	30	136	2717df78-59c8-4a55-ab69-243a983d222b	0	查询会话	2026-04-14 23:31:02.164532	2026-04-14 23:31:02.164533
会话详情	3	3	module_ai:chat:detail	\N	\N	\N	\N	\N	f	t	f	会话详情	null	f	30	137	5a8c86ba-2dc9-4583-b6da-1f089900a34c	0	会话详情	2026-04-14 23:31:02.164535	2026-04-14 23:31:02.164536
创建会话	3	4	module_ai:chat:create	\N	\N	\N	\N	\N	f	t	f	创建会话	null	f	30	138	2a80754a-1582-494d-b77a-196a96d38c12	0	创建会话	2026-04-14 23:31:02.164538	2026-04-14 23:31:02.164539
更新会话	3	5	module_ai:chat:update	\N	\N	\N	\N	\N	f	t	f	更新会话	null	f	30	139	c3d1ef1c-b782-4f3a-87a2-74c02cd75757	0	更新会话	2026-04-14 23:31:02.164542	2026-04-14 23:31:02.164542
删除会话	3	6	module_ai:chat:delete	\N	\N	\N	\N	\N	f	t	f	删除会话	null	f	30	140	00f75b5b-0d3e-47cf-9f04-4bb91c44faff	0	删除会话	2026-04-14 23:31:02.164545	2026-04-14 23:31:02.164545
查询会话记忆	3	1	module_ai:chat:query	\N	\N	\N	\N	\N	f	t	f	查询会话记忆	null	f	31	141	ee2abed1-1390-4abb-8815-80dbc4ab3145	0	查询会话记忆	2026-04-14 23:31:02.164548	2026-04-14 23:31:02.164548
会话记忆详情	3	2	module_ai:chat:detail	\N	\N	\N	\N	\N	f	t	f	会话记忆详情	null	f	31	142	896d90e8-1faf-4069-b756-26cdefdb2e99	0	会话记忆详情	2026-04-14 23:31:02.164551	2026-04-14 23:31:02.164551
删除会话记忆	3	3	module_ai:chat:delete	\N	\N	\N	\N	\N	f	t	f	删除会话记忆	null	f	31	143	09686ace-2d40-4d81-8b1c-be0a13d9e68b	0	删除会话记忆	2026-04-14 23:31:02.164554	2026-04-14 23:31:02.164555
调度器监控	2	1	module_task:cronjob:job:query	el-icon-DataLine	Job	/task/cronjob/job	module_task/cronjob/job/index	\N	f	t	f	调度器监控	null	f	32	144	b288c909-88f3-46e7-b267-515a394f7bc9	0	调度器监控	2026-04-14 23:31:02.164557	2026-04-14 23:31:02.164558
节点管理	2	2	module_task:cronjob:node:query	el-icon-Postcard	Node	/task/cronjob/node	module_task/cronjob/node/index	\N	f	t	f	节点管理	null	f	32	145	6bced9a1-9c16-4d4b-b38f-f2b474e41442	0	节点管理	2026-04-14 23:31:02.16456	2026-04-14 23:31:02.164561
流程编排	2	1	module_task:workflow:definition:query	el-icon-SetUp	Workflow	/task/workflow/definition	module_task/workflow/definition/index	\N	f	t	f	流程编排	null	f	33	146	0ddea6c3-ff4d-4e8e-b2b6-8a90cf444a7b	0	Vue Flow 画布与发布执行	2026-04-14 23:31:02.164563	2026-04-14 23:31:02.164564
编排节点类型	2	2	module_task:workflow:node-type:query	el-icon-Grid	WorkflowNodeType	/task/workflow/node-type	module_task/workflow/node-type/index	\N	f	t	f	编排节点类型	null	f	33	147	e3bad39c-0d8a-4c7b-9e80-2b16795e5210	0	画布节点类型与 Prefect 执行逻辑	2026-04-14 23:31:02.164567	2026-04-14 23:31:02.164567
创建示例	3	1	module_example:demo:create	\N	\N	\N	\N	\N	f	t	f	创建示例	null	f	34	148	61371d0d-93b9-4473-aff3-72898e80c1f3	0	初始化数据	2026-04-14 23:31:02.16457	2026-04-14 23:31:02.16457
更新示例	3	2	module_example:demo:update	\N	\N	\N	\N	\N	f	t	f	更新示例	null	f	34	149	85ecc201-91c6-4ae3-9756-9e6859fa8404	0	初始化数据	2026-04-14 23:31:02.164573	2026-04-14 23:31:02.164573
删除示例	3	3	module_example:demo:delete	\N	\N	\N	\N	\N	f	t	f	删除示例	null	f	34	150	a787aff3-8ec9-4b9f-8f56-8f16a043714e	0	初始化数据	2026-04-14 23:31:02.164576	2026-04-14 23:31:02.164576
批量修改示例状态	3	4	module_example:demo:patch	\N	\N	\N	\N	\N	f	t	f	批量修改示例状态	null	f	34	151	912be02f-b338-4689-9181-f06f1a1627a9	0	初始化数据	2026-04-14 23:31:02.164579	2026-04-14 23:31:02.164579
导出示例	3	5	module_example:demo:export	\N	\N	\N	\N	\N	f	t	f	导出示例	null	f	34	152	1ea4c990-22fa-45e8-bdcd-d0b8a2c019fd	0	初始化数据	2026-04-14 23:31:02.164582	2026-04-14 23:31:02.164582
导入示例	3	6	module_example:demo:import	\N	\N	\N	\N	\N	f	t	f	导入示例	null	f	34	153	5f1b5022-852e-4395-a051-074ef2f0b7cb	0	初始化数据	2026-04-14 23:31:02.164585	2026-04-14 23:31:02.164585
下载导入示例模版	3	7	module_example:demo:download	\N	\N	\N	\N	\N	f	t	f	下载导入示例模版	null	f	34	154	a8d864b0-7a5a-4d08-8184-3515d1853a1a	0	初始化数据	2026-04-14 23:31:02.164588	2026-04-14 23:31:02.164588
详情示例	3	8	module_example:demo:detail	\N	\N	\N	\N	\N	f	t	f	详情示例	null	f	34	155	32774640-45d3-4171-809e-1874e05cb6a2	0	初始化数据	2026-04-14 23:31:02.164591	2026-04-14 23:31:02.164592
查询示例	3	9	module_example:demo:query	\N	\N	\N	\N	\N	f	t	f	查询示例	null	f	34	156	13295da0-e955-4ed1-aa88-3681548511fb	0	初始化数据	2026-04-14 23:31:02.164594	2026-04-14 23:31:02.164595
三级菜单	2	1	module_example:demo01:query	menu	Demo01	/example/demo-group/demo01	module_example/demo01/index	\N	f	t	f	三级菜单	null	f	35	157	286ad567-1314-4047-92e0-bb9edfbcae6f	0	示例01管理	2026-04-14 23:31:02.164597	2026-04-14 23:31:02.164598
查询调度器	3	1	module_task:cronjob:job:query	\N	\N	\N	\N	\N	f	t	f	查询调度器	null	f	144	158	7461b147-a6f8-4c12-b0ab-86b57244d70c	0	查询调度器	2026-04-14 23:31:02.174698	2026-04-14 23:31:02.174702
控制调度器	3	2	module_task:cronjob:job:scheduler	\N	\N	\N	\N	\N	f	t	f	控制调度器	null	f	144	159	84f2c0bd-2638-405a-ae5c-ba943a4a54bd	0	控制调度器	2026-04-14 23:31:02.174706	2026-04-14 23:31:02.174706
操作任务	3	3	module_task:cronjob:job:task	\N	\N	\N	\N	\N	f	t	f	操作任务	null	f	144	160	3c8c14b8-3010-463b-b11c-6125e487eb8e	0	操作任务	2026-04-14 23:31:02.174709	2026-04-14 23:31:02.17471
删除执行日志	3	4	module_task:cronjob:job:delete	\N	\N	\N	\N	\N	f	t	f	删除执行日志	null	f	144	161	1f7590f9-87aa-46c6-877f-ea8904cd08ba	0	删除执行日志	2026-04-14 23:31:02.174713	2026-04-14 23:31:02.174713
详情执行日志	3	5	module_task:cronjob:job:detail	\N	\N	\N	\N	\N	f	t	f	详情执行日志	null	f	144	162	64cf74ff-8e50-4f6d-a7af-229923c7a336	0	详情执行日志	2026-04-14 23:31:02.174716	2026-04-14 23:31:02.174716
创建节点	3	1	module_task:cronjob:node:create	\N	\N	\N	\N	\N	f	t	f	创建节点	null	f	145	163	ecec4a51-13a3-4ba4-bcdf-a0742ad703dc	0	创建节点	2026-04-14 23:31:02.174719	2026-04-14 23:31:02.17472
调试节点	3	2	module_task:cronjob:node:execute	\N	\N	\N	\N	\N	f	t	f	调试节点	null	f	145	164	48e9a581-20fb-46fe-ba7b-3de150f2acb2	0	调试节点	2026-04-14 23:31:02.174722	2026-04-14 23:31:02.174723
修改节点	3	3	module_task:cronjob:node:update	\N	\N	\N	\N	\N	f	t	f	修改节点	null	f	145	165	52f3ced8-f716-466e-bc95-d96df2026239	0	修改节点	2026-04-14 23:31:02.174726	2026-04-14 23:31:02.174726
删除节点	3	4	module_task:cronjob:node:delete	\N	\N	\N	\N	\N	f	t	f	删除节点	null	f	145	166	512b1c7a-33fa-48f0-8524-12e512f55b56	0	删除节点	2026-04-14 23:31:02.174729	2026-04-14 23:31:02.17473
详情节点	3	5	module_task:cronjob:node:detail	\N	\N	\N	\N	\N	f	t	f	详情节点	null	f	145	167	6baf89aa-6be2-4c52-9e27-9bfc08124a4d	0	详情节点	2026-04-14 23:31:02.174732	2026-04-14 23:31:02.174733
查询节点	3	6	module_task:cronjob:node:query	\N	\N	\N	\N	\N	f	t	f	查询节点	null	f	145	168	ccef299d-c517-4162-a8c9-766aef78a855	0	查询节点	2026-04-14 23:31:02.174736	2026-04-14 23:31:02.174736
创建流程	3	1	module_task:workflow:definition:create	\N	\N	\N	\N	\N	f	t	f	创建流程	null	f	146	169	f1ea4737-17a2-46b0-8b9f-dd89299c6ecd	0	创建流程	2026-04-14 23:31:02.174739	2026-04-14 23:31:02.174739
执行流程	3	2	module_task:workflow:definition:execute	\N	\N	\N	\N	\N	f	t	f	执行流程	null	f	146	170	44c856c7-97c9-4b7c-8249-98734e1d2781	0	执行流程	2026-04-14 23:31:02.174742	2026-04-14 23:31:02.174742
修改流程	3	3	module_task:workflow:definition:update	\N	\N	\N	\N	\N	f	t	f	修改流程	null	f	146	171	a6f69185-17b1-453b-8c11-d09ab4febde4	0	修改流程	2026-04-14 23:31:02.174745	2026-04-14 23:31:02.174746
删除流程	3	4	module_task:workflow:definition:delete	\N	\N	\N	\N	\N	f	t	f	删除流程	null	f	146	172	b6039e19-08b4-437d-be9c-971a41a14375	0	删除流程	2026-04-14 23:31:02.174749	2026-04-14 23:31:02.174749
详情流程	3	5	module_task:workflow:definition:detail	\N	\N	\N	\N	\N	f	t	f	详情流程	null	f	146	173	d806fdbe-8350-48f3-bf2d-fba713cabdd8	0	详情流程	2026-04-14 23:31:02.174752	2026-04-14 23:31:02.174752
查询流程	3	6	module_task:workflow:definition:query	\N	\N	\N	\N	\N	f	t	f	查询流程	null	f	146	174	2db65f91-d0df-4bcb-989b-5658afcf3614	0	查询流程	2026-04-14 23:31:02.174755	2026-04-14 23:31:02.174755
创建编排节点类型	3	1	module_task:workflow:node-type:create	\N	\N	\N	\N	\N	f	t	f	创建编排节点类型	null	f	147	175	4115c587-d0da-417f-bf9a-410b48c7c2b0	0	创建编排节点类型	2026-04-14 23:31:02.174758	2026-04-14 23:31:02.174758
修改编排节点类型	3	2	module_task:workflow:node-type:update	\N	\N	\N	\N	\N	f	t	f	修改编排节点类型	null	f	147	176	ee3244d7-d9fc-42ce-a276-9619ddb131a8	0	修改编排节点类型	2026-04-14 23:31:02.174761	2026-04-14 23:31:02.174761
删除编排节点类型	3	3	module_task:workflow:node-type:delete	\N	\N	\N	\N	\N	f	t	f	删除编排节点类型	null	f	147	177	f2db26b9-481c-4f2c-ae39-33f4d5005172	0	删除编排节点类型	2026-04-14 23:31:02.174764	2026-04-14 23:31:02.174764
详情编排节点类型	3	4	module_task:workflow:node-type:detail	\N	\N	\N	\N	\N	f	t	f	详情编排节点类型	null	f	147	178	f209486d-8dc3-47e5-b581-20f143becff3	0	详情编排节点类型	2026-04-14 23:31:02.174767	2026-04-14 23:31:02.174768
查询编排节点类型	3	5	module_task:workflow:node-type:query	\N	\N	\N	\N	\N	f	t	f	查询编排节点类型	null	f	147	179	7dfcced4-5deb-438a-aa43-4af622e7c261	0	查询编排节点类型	2026-04-14 23:31:02.17477	2026-04-14 23:31:02.174771
创建示例01	3	1	module_example:demo01:create	\N	\N	\N	\N	\N	f	t	f	创建示例01	null	f	157	180	abeb9466-f231-41ff-a6e3-8173f828e1da	0	初始化数据	2026-04-14 23:31:02.174773	2026-04-14 23:31:02.174774
更新示例01	3	2	module_example:demo01:update	\N	\N	\N	\N	\N	f	t	f	更新示例01	null	f	157	181	b293feb4-3a62-4fd8-8d60-9eecd97d4f1e	0	初始化数据	2026-04-14 23:31:02.174776	2026-04-14 23:31:02.174777
删除示例01	3	3	module_example:demo01:delete	\N	\N	\N	\N	\N	f	t	f	删除示例01	null	f	157	182	de42d5bb-7a37-4d21-b14b-46fe1fe50872	0	初始化数据	2026-04-14 23:31:02.17478	2026-04-14 23:31:02.17478
批量修改示例01状态	3	4	module_example:demo01:patch	\N	\N	\N	\N	\N	f	t	f	批量修改示例01状态	null	f	157	183	d9de3f37-f765-43ea-a66d-be93f4341dbd	0	初始化数据	2026-04-14 23:31:02.174783	2026-04-14 23:31:02.174783
导出示例01	3	5	module_example:demo01:export	\N	\N	\N	\N	\N	f	t	f	导出示例01	null	f	157	184	936a5dd0-3138-4659-98f1-3923400e248b	0	初始化数据	2026-04-14 23:31:02.174786	2026-04-14 23:31:02.174786
导入示例01	3	6	module_example:demo01:import	\N	\N	\N	\N	\N	f	t	f	导入示例01	null	f	157	185	237e58f0-60e1-4b1e-81dd-9e00888da9cb	0	初始化数据	2026-04-14 23:31:02.174789	2026-04-14 23:31:02.174789
下载导入示例01模版	3	7	module_example:demo01:download	\N	\N	\N	\N	\N	f	t	f	下载导入示例01模版	null	f	157	186	27d82f1a-65b3-4e0b-93bf-e90b75562e26	0	初始化数据	2026-04-14 23:31:02.174792	2026-04-14 23:31:02.174792
详情示例01	3	8	module_example:demo01:detail	\N	\N	\N	\N	\N	f	t	f	详情示例01	null	f	157	187	74b14385-1c15-431d-a759-8f3a0fdf66ac	0	初始化数据	2026-04-14 23:31:02.174795	2026-04-14 23:31:02.174795
查询示例01	3	9	module_example:demo01:query	\N	\N	\N	\N	\N	f	t	f	查询示例01	null	f	157	188	3f9d5efb-d648-4b89-b653-c2f27f62a381	0	初始化数据	2026-04-14 23:31:02.174798	2026-04-14 23:31:02.174798
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
网站名称	sys_web_title	FastApiAdmin	t	1	9339f899-df87-4dae-b5c4-9325922b4094	0	初始化数据	2026-04-14 23:31:02.181076	2026-04-14 23:31:02.181078
网站描述	sys_web_description	FastApiAdmin 是完全开源的权限管理系统	t	2	98c9aeef-7ee3-44c7-bcd2-a6206ce87d5c	0	初始化数据	2026-04-14 23:31:02.181082	2026-04-14 23:31:02.181083
网页图标	sys_web_favicon	https://service.fastapiadmin.com/api/v1/static/image/favicon.png	t	3	a9b2ccb2-0a9a-4e66-b98a-f8a73faa9fc5	0	初始化数据	2026-04-14 23:31:02.181086	2026-04-14 23:31:02.181086
网站Logo	sys_web_logo	https://service.fastapiadmin.com/api/v1/static/image/logo.png	t	4	6a522c66-6703-4c97-aa43-daf051e5e372	0	初始化数据	2026-04-14 23:31:02.181089	2026-04-14 23:31:02.181089
登录背景	sys_login_background	https://service.fastapiadmin.com/api/v1/static/image/background.svg	t	5	500ef266-852e-468c-93ff-b5ca5af6641f	0	初始化数据	2026-04-14 23:31:02.181092	2026-04-14 23:31:02.181092
版权信息	sys_web_copyright	Copyright © 2025-2026 service.fastapiadmin.com 版权所有	t	6	330b93ea-37df-4909-a5fc-9b43af363c05	0	初始化数据	2026-04-14 23:31:02.181095	2026-04-14 23:31:02.181095
备案信息	sys_keep_record	陕ICP备2025069493号-1	t	7	16347b99-2c17-442f-95e6-24d8792f7180	0	初始化数据	2026-04-14 23:31:02.181098	2026-04-14 23:31:02.181098
帮助文档	sys_help_doc	https://service.fastapiadmin.com	t	8	a93cecc1-0f42-4e4c-8bcd-6cf092da4795	0	初始化数据	2026-04-14 23:31:02.181101	2026-04-14 23:31:02.181102
隐私政策	sys_web_privacy	https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE	t	9	e79e3c07-40c8-4084-a220-1db08d9a6535	0	初始化数据	2026-04-14 23:31:02.181104	2026-04-14 23:31:02.181105
用户协议	sys_web_clause	https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE	t	10	ea0eb8ab-e752-4b6a-8f36-feb9c724b2fe	0	初始化数据	2026-04-14 23:31:02.181107	2026-04-14 23:31:02.181108
源码代码	sys_git_code	https://github.com/fastapiadmin/FastapiAdmin.git	t	11	8a7bfead-93a2-4fba-9ea0-c9c417731d82	0	初始化数据	2026-04-14 23:31:02.18111	2026-04-14 23:31:02.181111
项目版本	sys_web_version	2.0.0	t	12	25ea6bb8-f821-49d8-81fb-e277e6b99f92	0	初始化数据	2026-04-14 23:31:02.181113	2026-04-14 23:31:02.181114
演示模式启用	demo_enable	false	t	13	37274a20-3f2b-4cf5-b2f1-ceeee0bad555	0	初始化数据	2026-04-14 23:31:02.181116	2026-04-14 23:31:02.181117
演示访问IP白名单	ip_white_list	["127.0.0.1"]	t	14	ea3e4a0e-fd11-45a7-bb93-fe8f195b46f5	0	初始化数据	2026-04-14 23:31:02.181119	2026-04-14 23:31:02.18112
接口白名单	white_api_list_path	["/api/v1/system/auth/login", "/api/v1/system/auth/token/refresh", "/api/v1/system/auth/captcha/get", "/api/v1/system/auth/logout", "/api/v1/system/config/info", "/api/v1/system/user/current/info", "/api/v1/system/notice/available", "/api/v1/system/auth/auto-login/users", "/api/v1/system/auth/auto-login/token", "/api/v1/system/auth/auto-login"]	t	15	70ab9a3f-fe9e-4b5a-9203-91f9f562d10b	0	初始化数据	2026-04-14 23:31:02.181122	2026-04-14 23:31:02.181123
访问IP黑名单	ip_black_list	[]	t	16	164400d2-3371-45e0-aec8-a49969d1950f	0	初始化数据	2026-04-14 23:31:02.181125	2026-04-14 23:31:02.181126
调度器状态	scheduler_status	stopped	t	17	7bcde4d1-bb1f-4d03-bffd-277cde46e85d	0	\N	2026-04-14 23:31:05.847007	2026-04-14 23:31:05.847012
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
管理员角色	ADMIN	1	4	1	c827090f-3ee6-4930-a1a9-9a16ae29a048	0	初始化角色	2026-04-14 23:31:02.18962	2026-04-14 23:31:02.189623
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
-- Data for Name: sys_tenant; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_tenant (name, code, start_time, end_time, id, uuid, status, description, created_time, updated_time) FROM stdin;
系统租户	system	\N	\N	1	a47fbad2-071e-4db5-95b1-e5ad16141c39	0	平台默认租户，id 固定为 1	2026-04-14 23:31:02.137829	2026-04-14 23:31:02.137832
\.


--
-- Data for Name: sys_user; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.sys_user (username, password, name, mobile, email, gender, avatar, is_superuser, last_login, gitee_login, github_login, wx_login, qq_login, dept_id, id, uuid, status, description, created_time, updated_time, tenant_id, created_id, updated_id) FROM stdin;
admin	$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa	超级管理员	\N	\N	0	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	t	\N	\N	\N	\N	\N	1	1	4ca29544-2199-4570-b45b-28bbd5ac53a5	0	超级管理员	2026-04-14 23:31:02.206591	2026-04-14 23:31:02.206592	1	\N	\N
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

SELECT pg_catalog.setval('public.sys_menu_id_seq', 188, true);


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
-- Name: sys_tenant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.sys_tenant_id_seq', 1, true);


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
-- Name: sys_dept sys_dept_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_code_key UNIQUE (code);


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
-- Name: sys_role sys_role_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_role
    ADD CONSTRAINT sys_role_code_key UNIQUE (code);


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
-- Name: sys_tenant sys_tenant_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_tenant
    ADD CONSTRAINT sys_tenant_code_key UNIQUE (code);


--
-- Name: sys_tenant sys_tenant_name_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_tenant
    ADD CONSTRAINT sys_tenant_name_key UNIQUE (name);


--
-- Name: sys_tenant sys_tenant_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_tenant
    ADD CONSTRAINT sys_tenant_pkey PRIMARY KEY (id);


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
-- Name: ix_app_portal_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_app_portal_tenant_id ON public.app_portal USING btree (tenant_id);


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
-- Name: ix_sys_tenant_created_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_tenant_created_time ON public.sys_tenant USING btree (created_time);


--
-- Name: ix_sys_tenant_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_tenant_id ON public.sys_tenant USING btree (id);


--
-- Name: ix_sys_tenant_status; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_tenant_status ON public.sys_tenant USING btree (status);


--
-- Name: ix_sys_tenant_updated_time; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_sys_tenant_updated_time ON public.sys_tenant USING btree (updated_time);


--
-- Name: ix_sys_tenant_uuid; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_sys_tenant_uuid ON public.sys_tenant USING btree (uuid);


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
-- Name: app_portal app_portal_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.app_portal
    ADD CONSTRAINT app_portal_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.sys_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


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
-- Name: sys_user sys_user_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.sys_tenant(id) ON UPDATE CASCADE ON DELETE RESTRICT;


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

\unrestrict MSeJP5WlbZL9YuY2N0b0zn88F8HQRuiwqrwhSdt3h8bn3cZtyhxMSVH7wTian01

