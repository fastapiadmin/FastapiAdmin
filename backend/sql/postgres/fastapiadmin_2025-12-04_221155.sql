--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (ServBay)
-- Dumped by pg_dump version 17.5 (ServBay)

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
-- Name: app_ai_mcp; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.app_ai_mcp (
    name character varying(50) NOT NULL,
    type integer NOT NULL,
    url character varying(255),
    command character varying(255),
    args character varying(255),
    env json,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.app_ai_mcp OWNER TO tao;

--
-- Name: TABLE app_ai_mcp; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.app_ai_mcp IS 'MCP 服务器表';


--
-- Name: COLUMN app_ai_mcp.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.name IS 'MCP 名称';


--
-- Name: COLUMN app_ai_mcp.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.type IS 'MCP 类型(0:stdio 1:sse)';


--
-- Name: COLUMN app_ai_mcp.url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.url IS '远程 SSE 地址';


--
-- Name: COLUMN app_ai_mcp.command; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.command IS 'MCP 命令';


--
-- Name: COLUMN app_ai_mcp.args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.args IS 'MCP 命令参数';


--
-- Name: COLUMN app_ai_mcp.env; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.env IS 'MCP 环境变量';


--
-- Name: COLUMN app_ai_mcp.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.id IS '主键ID';


--
-- Name: COLUMN app_ai_mcp.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN app_ai_mcp.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN app_ai_mcp.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.description IS '备注/描述';


--
-- Name: COLUMN app_ai_mcp.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.created_time IS '创建时间';


--
-- Name: COLUMN app_ai_mcp.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.updated_time IS '更新时间';


--
-- Name: COLUMN app_ai_mcp.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.created_id IS '创建人ID';


--
-- Name: COLUMN app_ai_mcp.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.updated_id IS '更新人ID';


--
-- Name: app_ai_mcp_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.app_ai_mcp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.app_ai_mcp_id_seq OWNER TO tao;

--
-- Name: app_ai_mcp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.app_ai_mcp_id_seq OWNED BY public.app_ai_mcp.id;


--
-- Name: app_job; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.app_job (
    name character varying(64),
    jobstore character varying(64),
    executor character varying(64),
    trigger character varying(64) NOT NULL,
    trigger_args text,
    func text NOT NULL,
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


ALTER TABLE public.app_job OWNER TO tao;

--
-- Name: TABLE app_job; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.app_job IS '定时任务调度表';


--
-- Name: COLUMN app_job.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.name IS '任务名称';


--
-- Name: COLUMN app_job.jobstore; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.jobstore IS '存储器';


--
-- Name: COLUMN app_job.executor; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.executor IS '执行器:将运行此作业的执行程序的名称';


--
-- Name: COLUMN app_job.trigger; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.trigger IS '触发器:控制此作业计划的 trigger 对象';


--
-- Name: COLUMN app_job.trigger_args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.trigger_args IS '触发器参数';


--
-- Name: COLUMN app_job.func; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.func IS '任务函数';


--
-- Name: COLUMN app_job.args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.args IS '位置参数';


--
-- Name: COLUMN app_job.kwargs; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.kwargs IS '关键字参数';


--
-- Name: COLUMN app_job."coalesce"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job."coalesce" IS '是否合并运行:是否在多个运行时间到期时仅运行作业一次';


--
-- Name: COLUMN app_job.max_instances; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.max_instances IS '最大实例数:允许的最大并发执行实例数';


--
-- Name: COLUMN app_job.start_date; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.start_date IS '开始时间';


--
-- Name: COLUMN app_job.end_date; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.end_date IS '结束时间';


--
-- Name: COLUMN app_job.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.id IS '主键ID';


--
-- Name: COLUMN app_job.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN app_job.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN app_job.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.description IS '备注/描述';


--
-- Name: COLUMN app_job.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.created_time IS '创建时间';


--
-- Name: COLUMN app_job.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.updated_time IS '更新时间';


--
-- Name: COLUMN app_job.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.created_id IS '创建人ID';


--
-- Name: COLUMN app_job.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.updated_id IS '更新人ID';


--
-- Name: app_job_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.app_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.app_job_id_seq OWNER TO tao;

--
-- Name: app_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.app_job_id_seq OWNED BY public.app_job.id;


--
-- Name: app_job_log; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.app_job_log (
    job_name character varying(64) NOT NULL,
    job_group character varying(64) NOT NULL,
    job_executor character varying(64) NOT NULL,
    invoke_target character varying(500) NOT NULL,
    job_args character varying(255),
    job_kwargs character varying(255),
    job_trigger character varying(255),
    job_message character varying(500),
    exception_info character varying(2000),
    job_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.app_job_log OWNER TO tao;

--
-- Name: TABLE app_job_log; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.app_job_log IS '定时任务调度日志表';


--
-- Name: COLUMN app_job_log.job_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_name IS '任务名称';


--
-- Name: COLUMN app_job_log.job_group; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_group IS '任务组名';


--
-- Name: COLUMN app_job_log.job_executor; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_executor IS '任务执行器';


--
-- Name: COLUMN app_job_log.invoke_target; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.invoke_target IS '调用目标字符串';


--
-- Name: COLUMN app_job_log.job_args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_args IS '位置参数';


--
-- Name: COLUMN app_job_log.job_kwargs; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_kwargs IS '关键字参数';


--
-- Name: COLUMN app_job_log.job_trigger; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_trigger IS '任务触发器';


--
-- Name: COLUMN app_job_log.job_message; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_message IS '日志信息';


--
-- Name: COLUMN app_job_log.exception_info; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.exception_info IS '异常信息';


--
-- Name: COLUMN app_job_log.job_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_id IS '任务ID';


--
-- Name: COLUMN app_job_log.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.id IS '主键ID';


--
-- Name: COLUMN app_job_log.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN app_job_log.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN app_job_log.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.description IS '备注/描述';


--
-- Name: COLUMN app_job_log.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.created_time IS '创建时间';


--
-- Name: COLUMN app_job_log.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.updated_time IS '更新时间';


--
-- Name: app_job_log_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.app_job_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.app_job_log_id_seq OWNER TO tao;

--
-- Name: app_job_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.app_job_log_id_seq OWNED BY public.app_job_log.id;


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
    name character varying(64),
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
    name character varying(40) NOT NULL,
    "order" integer NOT NULL,
    code character varying(20),
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
    dict_name character varying(255) NOT NULL,
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
    notice_title character varying(50) NOT NULL,
    notice_type character varying(50) NOT NULL,
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
    config_name character varying(500) NOT NULL,
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
    name character varying(40) NOT NULL,
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
    name character varying(40) NOT NULL,
    code character varying(20),
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
    username character varying(32) NOT NULL,
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
-- Name: app_ai_mcp id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_ai_mcp ALTER COLUMN id SET DEFAULT nextval('public.app_ai_mcp_id_seq'::regclass);


--
-- Name: app_job id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job ALTER COLUMN id SET DEFAULT nextval('public.app_job_id_seq'::regclass);


--
-- Name: app_job_log id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job_log ALTER COLUMN id SET DEFAULT nextval('public.app_job_log_id_seq'::regclass);


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
-- Data for Name: app_ai_mcp; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.app_ai_mcp (name, type, url, command, args, env, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: app_job; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.app_job (name, jobstore, executor, trigger, trigger_args, func, args, kwargs, "coalesce", max_instances, start_date, end_date, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: app_job_log; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.app_job_log (job_name, job_group, job_executor, invoke_target, job_args, job_kwargs, job_trigger, job_message, exception_info, job_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
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

COPY public.gen_demo (name, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
test1	3	7f0e50b5-ed5f-41c0-b6c1-a89e9bf1c33b	0	\N	2025-12-04 21:47:23.974321	2025-12-04 21:47:23.974325	2	2
test2	4	165c3e41-d9e8-4dcf-b5ad-ca393bb13c38	0	\N	2025-12-04 21:47:47.305899	2025-12-04 21:47:47.305903	3	3
test101	5	2d02f458-3b78-4e6b-a619-403b406d21f6	0	\N	2025-12-04 21:49:09.231903	2025-12-04 21:49:09.231944	4	4
test102	6	82437f97-65c0-4c9f-8d49-822e1e3010e9	0	\N	2025-12-04 21:49:39.159823	2025-12-04 21:49:39.15983	5	5
test201	7	b450605a-354c-4345-ae9c-4296454da490	0	\N	2025-12-04 21:50:19.006998	2025-12-04 21:50:19.007002	6	6
test202	8	6a340642-aca6-478a-9b8b-16b7f238e16c	0	\N	2025-12-04 21:50:50.105569	2025-12-04 21:50:50.105574	7	7
test22	9	f20abab2-39bb-4797-8d42-d46707b80c26	0	\N	2025-12-04 22:06:49.45593	2025-12-04 22:06:49.455936	8	8
\.


--
-- Data for Name: gen_table; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.gen_table (table_name, table_comment, class_name, package_name, module_name, business_name, function_name, sub_table_name, sub_table_fk_name, parent_menu_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
gen_demo	示例表	GenDemo	module_gencode	module_gencode	gen_demo	示例	\N	\N	\N	1	ea3370a7-9ffa-472f-a835-a5e787e84a11	0	\N	2025-12-04 20:48:26.212177	2025-12-04 20:48:26.212181	1	1
\.


--
-- Data for Name: gen_table_column; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.gen_table_column (column_name, column_comment, column_type, column_length, column_default, is_pk, is_increment, is_nullable, is_unique, python_type, python_field, is_insert, is_edit, is_list, is_query, query_type, html_type, dict_type, sort, table_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
name	名称	varchar	64		f	f	f	f	str	name	t	t	t	t	LIKE	input		1	1	1	ed471acf-3ea2-410c-9751-ed5fd8b379bf	0	\N	2025-12-04 20:48:26.265731	2025-12-04 20:48:26.265735	1	1
id	主键ID	int4		nextval('gen_demo_id_seq'::regclass)	t	t	t	f	int	id	t	f	f	f	\N	input		2	1	2	9a4f7dd6-912d-498c-b438-1eda1fa3ba9c	0	\N	2025-12-04 20:48:26.274154	2025-12-04 20:48:26.274158	1	1
uuid	UUID全局唯一标识	varchar	64		f	f	t	t	str	uuid	t	f	f	f	\N	input		3	1	3	ca6e8c47-fb53-48d6-8a96-223738f1341d	0	\N	2025-12-04 20:48:26.276079	2025-12-04 20:48:26.276082	1	1
description	备注/描述	text			f	f	f	f	str	description	t	f	f	f	\N	input		5	1	5	cc66ab04-d191-496d-950d-1eb252c4dc5e	0	\N	2025-12-04 20:48:26.279785	2025-12-04 20:48:26.279787	1	1
created_time	创建时间	timestamp			f	f	t	f	datetime	createdTime	t	f	f	f	\N	input		6	1	6	b59fc690-e38a-4467-ac7e-607761be32fd	0	\N	2025-12-04 20:48:26.281612	2025-12-04 20:48:26.281614	1	1
updated_time	更新时间	timestamp			f	f	t	f	datetime	updatedTime	t	f	f	f	\N	input		7	1	7	0437828b-9418-486b-9730-d80c80676a0f	0	\N	2025-12-04 20:48:26.28338	2025-12-04 20:48:26.283381	1	1
created_id	创建人ID	int4			f	f	f	f	int	createdId	t	t	t	t	EQ	input		8	1	8	e2f84c36-fe6e-4800-ba85-39bb5c9232b8	0	\N	2025-12-04 20:48:26.28515	2025-12-04 20:48:26.285151	1	1
updated_id	更新人ID	int4			f	f	f	f	int	updatedId	t	t	t	t	EQ	input		9	1	9	eaf874ef-be0b-44c3-828e-c35e8c3cdd76	0	\N	2025-12-04 20:48:26.287042	2025-12-04 20:48:26.287043	1	1
status	是否启用(0:启用 1:禁用)	varchar	10		f	f	t	f	str	status	t	t	t	t	EQ	input		4	1	4	5ccd94c8-66cf-4828-a97f-bb22f4adcc03	0	\N	2025-12-04 20:48:26.277905	2025-12-04 21:01:46.549167	1	1
\.


--
-- Data for Name: sys_dept; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_dept (name, "order", code, leader, phone, email, parent_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
集团总公司	1	GROUP	部门负责人	1582112620	deptadmin@example.com	\N	1	8b0a0481-23fd-45b6-bb77-44090af2db2d	0	集团总公司	2025-12-03 23:23:58.821858	2025-12-03 23:23:58.821859
test1	1	test1	\N	\N	\N	1	2	aa1ee42b-7369-49f6-badb-a3784f57bbfa	0	\N	2025-12-04 21:16:25.462323	2025-12-04 21:16:25.462327
test2	1	test2	\N	\N	\N	1	3	e765168f-6ade-4c5d-9c3f-7ba94cce5ade	0	\N	2025-12-04 21:16:35.816631	2025-12-04 21:16:35.816638
test1_1	1	test1_1	\N	\N	\N	2	4	0e9b15e1-acaa-4de6-974e-f59154ed7dde	0	\N	2025-12-04 21:16:46.521846	2025-12-04 21:16:46.521851
test1_2	1	test1_2	\N	\N	\N	2	5	07ef4871-5f55-49f0-87f0-1a9b28017c5c	0	\N	2025-12-04 21:17:23.723122	2025-12-04 21:17:23.723126
test2_2	1	test2_2	\N	\N	\N	3	6	8a640047-7c0f-42ef-84a1-0ec7d994d5ce	0	\N	2025-12-04 21:17:36.038884	2025-12-04 21:17:36.038888
test2_1	1	test2_1	\N	\N	\N	3	7	fee2602e-77ff-406b-8151-9774f3d99a07	0	\N	2025-12-04 21:17:46.888802	2025-12-04 21:17:46.888806
\.


--
-- Data for Name: sys_dict_data; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_dict_data (dict_sort, dict_label, dict_value, css_class, list_class, is_default, dict_type, dict_type_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
1	男	0	blue	\N	t	sys_user_sex	1	1	0b3f0bff-c57a-44c2-881d-4e4ad9f6a398	0	性别男	2025-12-03 23:23:58.832709	2025-12-03 23:23:58.832709
2	女	1	pink	\N	f	sys_user_sex	1	2	eb49d01b-c395-4be4-88ff-e5797b3a43f9	0	性别女	2025-12-03 23:23:58.832713	2025-12-03 23:23:58.832714
3	未知	2	red	\N	f	sys_user_sex	1	3	35e1fc6c-98e9-40d6-a7c4-a753014e4115	0	性别未知	2025-12-03 23:23:58.832716	2025-12-03 23:23:58.832717
1	是	1		primary	t	sys_yes_no	2	4	174fa595-e079-4c01-9670-65f28c5eba3b	0	是	2025-12-03 23:23:58.83272	2025-12-03 23:23:58.83272
2	否	0		danger	f	sys_yes_no	2	5	5b5bb1fd-d760-4c75-9622-96f8de5f2c91	0	否	2025-12-03 23:23:58.832723	2025-12-03 23:23:58.832723
1	启用	1		primary	f	sys_common_status	3	6	a812bf73-82b3-4aad-a3e2-609a37addb27	0	启用状态	2025-12-03 23:23:58.832725	2025-12-03 23:23:58.832726
2	停用	0		danger	f	sys_common_status	3	7	ef928718-b2cf-42d0-b628-5a9e3cb0dc39	0	停用状态	2025-12-03 23:23:58.832728	2025-12-03 23:23:58.832729
1	通知	1	blue	warning	t	sys_notice_type	4	8	2654c6fa-8df6-4ab6-8f3d-3d69a099cf61	0	通知	2025-12-03 23:23:58.832731	2025-12-03 23:23:58.832732
2	公告	2	orange	success	f	sys_notice_type	4	9	57b55dba-9b62-45e6-b833-4f9fac2076cf	0	公告	2025-12-03 23:23:58.832735	2025-12-03 23:23:58.832735
99	其他	0		info	f	sys_oper_type	5	10	94c5a5f2-2ea5-4d57-810a-6e251be0813f	0	其他操作	2025-12-03 23:23:58.832738	2025-12-03 23:23:58.832738
1	新增	1		info	f	sys_oper_type	5	11	686ea17f-a89c-496e-8f26-61e573a9f59b	0	新增操作	2025-12-03 23:23:58.832741	2025-12-03 23:23:58.832741
2	修改	2		info	f	sys_oper_type	5	12	f760f42b-a149-47f0-bded-4de70704caf7	0	修改操作	2025-12-03 23:23:58.832744	2025-12-03 23:23:58.832744
3	删除	3		danger	f	sys_oper_type	5	13	203e973c-ff8e-4885-9ea8-5b356582470f	0	删除操作	2025-12-03 23:23:58.832747	2025-12-03 23:23:58.832747
4	分配权限	4		primary	f	sys_oper_type	5	14	00ad2e1a-c727-4b8f-b2c8-2cc0d636de0a	0	授权操作	2025-12-03 23:23:58.83275	2025-12-03 23:23:58.83275
5	导出	5		warning	f	sys_oper_type	5	15	25fa1c5f-80a5-49bf-aa94-f0dec3f1dab9	0	导出操作	2025-12-03 23:23:58.832753	2025-12-03 23:23:58.832753
6	导入	6		warning	f	sys_oper_type	5	16	2fc58ed1-b30a-4d69-893d-c29be1226ea0	0	导入操作	2025-12-03 23:23:58.832756	2025-12-03 23:23:58.832757
7	强退	7		danger	f	sys_oper_type	5	17	4b09e884-a551-4010-926d-af82cd844731	0	强退操作	2025-12-03 23:23:58.832759	2025-12-03 23:23:58.832759
8	生成代码	8		warning	f	sys_oper_type	5	18	eabcc4f5-3b9e-4e18-88f3-652b96e36ecf	0	生成操作	2025-12-03 23:23:58.832762	2025-12-03 23:23:58.832762
9	清空数据	9		danger	f	sys_oper_type	5	19	efba94c1-10c0-4c71-9998-f407a7e3a907	0	清空操作	2025-12-03 23:23:58.832765	2025-12-03 23:23:58.832765
1	默认(Memory)	default		\N	t	sys_job_store	6	20	13868e0a-073e-428d-b2f8-6ad7e9919261	0	默认分组	2025-12-03 23:23:58.832768	2025-12-03 23:23:58.832768
2	数据库(Sqlalchemy)	sqlalchemy		\N	f	sys_job_store	6	21	bc934f0c-0ef6-4ec5-9f79-b3ea8529f9b2	0	数据库分组	2025-12-03 23:23:58.832771	2025-12-03 23:23:58.832771
3	数据库(Redis)	redis		\N	f	sys_job_store	6	22	2749b237-fd04-48bf-a816-31192d286788	0	reids分组	2025-12-03 23:23:58.832774	2025-12-03 23:23:58.832774
1	线程池	default		\N	f	sys_job_executor	7	23	19faea4e-daf5-4bd5-8d98-0f0c930943b8	0	线程池	2025-12-03 23:23:58.832777	2025-12-03 23:23:58.832777
2	进程池	processpool		\N	f	sys_job_executor	7	24	3a453e57-982f-4722-b39d-f9884547163e	0	进程池	2025-12-03 23:23:58.83278	2025-12-03 23:23:58.83278
1	演示函数	scheduler_test.job		\N	t	sys_job_function	8	25	c8c1ff2c-52ba-4057-93d6-23ddec668a28	0	演示函数	2025-12-03 23:23:58.832783	2025-12-03 23:23:58.832783
1	指定日期(date)	date		\N	t	sys_job_trigger	9	26	7a5e96ce-5980-4c16-9776-1ed48de55e3b	0	指定日期任务触发器	2025-12-03 23:23:58.832786	2025-12-03 23:23:58.832786
2	间隔触发器(interval)	interval		\N	f	sys_job_trigger	9	27	66aebdfb-7cea-4dc6-8b2d-bf9add2df341	0	间隔触发器任务触发器	2025-12-03 23:23:58.832789	2025-12-03 23:23:58.832789
3	cron表达式	cron		\N	f	sys_job_trigger	9	28	5fabdca5-1251-4242-85ac-c08380dd3083	0	间隔触发器任务触发器	2025-12-03 23:23:58.832792	2025-12-03 23:23:58.832792
1	默认(default)	default		\N	t	sys_list_class	10	29	a62aa8b2-1f8f-41e5-960f-6ac19d2b7e1f	0	默认表格回显样式	2025-12-03 23:23:58.832795	2025-12-03 23:23:58.832796
2	主要(primary)	primary		\N	f	sys_list_class	10	30	4c82d704-e93e-4878-85e9-42885ea3ce8d	0	主要表格回显样式	2025-12-03 23:23:58.832798	2025-12-03 23:23:58.832799
3	成功(success)	success		\N	f	sys_list_class	10	31	2b09b4ac-28fe-4b92-9be6-461a973cde3a	0	成功表格回显样式	2025-12-03 23:23:58.832801	2025-12-03 23:23:58.832802
4	信息(info)	info		\N	f	sys_list_class	10	32	c9f61fa5-88fe-406f-898a-7b33c4fd6f6a	0	信息表格回显样式	2025-12-03 23:23:58.832804	2025-12-03 23:23:58.832805
5	警告(warning)	warning		\N	f	sys_list_class	10	33	429886da-72d8-440f-9c48-7d1ffcd63cd3	0	警告表格回显样式	2025-12-03 23:23:58.832807	2025-12-03 23:23:58.832807
6	危险(danger)	danger		\N	f	sys_list_class	10	34	b252ba68-b6cc-408c-bc80-948b55a7ec9c	0	危险表格回显样式	2025-12-03 23:23:58.83281	2025-12-03 23:23:58.83281
\.


--
-- Data for Name: sys_dict_type; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_dict_type (dict_name, dict_type, id, uuid, status, description, created_time, updated_time) FROM stdin;
用户性别	sys_user_sex	1	bb817f0f-fe0c-4342-87b7-89bc04c3e329	0	用户性别列表	2025-12-03 23:23:58.828998	2025-12-03 23:23:58.829
系统是否	sys_yes_no	2	c00c70d7-6a29-4c48-86d4-aab30a833ea0	0	系统是否列表	2025-12-03 23:23:58.829007	2025-12-03 23:23:58.829008
系统状态	sys_common_status	3	055ce947-24ad-4870-a682-4f6b431b8b95	0	系统状态	2025-12-03 23:23:58.829011	2025-12-03 23:23:58.829012
通知类型	sys_notice_type	4	abc9709a-0ebe-4f45-a6ca-884d9a23817a	0	通知类型列表	2025-12-03 23:23:58.829015	2025-12-03 23:23:58.829015
操作类型	sys_oper_type	5	b9b28cf5-5beb-4e73-879f-21cd13baf902	0	操作类型列表	2025-12-03 23:23:58.829018	2025-12-03 23:23:58.829019
任务存储器	sys_job_store	6	01812c5b-f12c-45bd-b532-edc18f40a0fa	0	任务分组列表	2025-12-03 23:23:58.829021	2025-12-03 23:23:58.829022
任务执行器	sys_job_executor	7	44abbce0-154c-4633-a105-bfc07588aa44	0	任务执行器列表	2025-12-03 23:23:58.829025	2025-12-03 23:23:58.829025
任务函数	sys_job_function	8	80fed07a-d3b9-4fef-b204-b4a99b3bcd17	0	任务函数列表	2025-12-03 23:23:58.829028	2025-12-03 23:23:58.829028
任务触发器	sys_job_trigger	9	cbbca7ef-11c8-469e-855f-da832aab8c1a	0	任务触发器列表	2025-12-03 23:23:58.829031	2025-12-03 23:23:58.829031
表格回显样式	sys_list_class	10	df8bdf53-bb8a-437f-a3a3-d07e44f08c11	0	表格回显样式列表	2025-12-03 23:23:58.829034	2025-12-03 23:23:58.829035
\.


--
-- Data for Name: sys_log; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_log (type, request_path, request_method, request_payload, request_ip, login_location, request_os, request_browser, response_code, response_json, process_time, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
2	/api/v1/system/user/create	POST	{"body": {"username": "test1", "name": "test1", "dept_id": 1, "role_ids": [1], "password": "123456", "is_superuser": false, "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建用户成功","data":{"created_id":1,"created_by":null,"updated_id":1,"updated_by":null,"id":2,"uuid":"3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29","status":"0","description":null,"created_time":"2025-12-03 23:24:32","updated_time":"2025-12-03 23:24:32","name":"test1","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1","password":"$2b$12$uq73vy/IxcGdIpVcm1Ktsu2pJh7bRllZk7jn2Yd2Q30DEdbhHLX5a","is_superuser":false,"dept_id":1,"role_ids":[],"position_ids":[],"last_login":null,"gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":1,"name":"集团总公司"},"positions":[],"roles":[{"id":1,"uuid":"f775fc7c-2643-4feb-a647-182f293b7952","status":"0","description":"初始化角色","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"管理员角色","code":"ADMIN","order":1,"data_scope":4,"menus":[],"depts":[]}],"menus":[]},"status_code":200,"success":true}	0.46s	1	63d1aafc-6ac7-46fe-b183-6107d2bd7649	0	创建用户	2025-12-03 23:24:32.800624	2025-12-03 23:24:32.800626	1	1
2	/api/v1/gencode/demo/create	POST	{"body": {"name": "test", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建示例成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":1,"uuid":"a2f932d2-489e-443b-ae09-373b409eb3e9","status":"0","description":null,"created_time":"2025-12-03 23:31:50","updated_time":"2025-12-03 23:31:50","name":"test"},"status_code":200,"success":true}	0.04s	2	bc46e03f-5646-4d10-a0ee-38e5463af6f2	0	创建示例	2025-12-03 23:31:50.158446	2025-12-03 23:31:50.158448	1	1
2	/api/v1/gencode/demo/create	POST	{"body": {"name": "test1", "status": "0", "description": ""}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建示例成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":2,"uuid":"412fc32c-50a4-49dd-80eb-3488547e20ae","status":"0","description":"","created_time":"2025-12-03 23:31:59","updated_time":"2025-12-03 23:31:59","name":"test1"},"status_code":200,"success":true}	0.03s	3	f894b32e-3395-462c-9134-9c2d327ea523	0	创建示例	2025-12-03 23:31:59.913139	2025-12-03 23:31:59.913141	1	1
2	/api/v1/generator/gencode/import	POST	{"body": ["gen_demo"]}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"导入表结构成功","data":true,"status_code":200,"success":true}	0.14s	4	6a7c4244-dfeb-42ef-b11c-dbd99337eb9c	0	导入表结构	2025-12-04 20:48:26.323453	2025-12-04 20:48:26.323458	1	1
2	/api/v1/generator/gencode/update/1	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"编辑业务表信息成功","data":{"id":1,"uuid":"ea3370a7-9ffa-472f-a835-a5e787e84a11","status":"0","description":null,"created_time":"2025-12-04 20:48:26","updated_time":"2025-12-04 20:48:26","table_name":"gen_demo","table_comment":"示例表","class_name":"GenDemo","package_name":"module_gencode","module_name":"module_gencode","business_name":"gen_demo","function_name":"示例","sub_table_name":null,"sub_table_fk_name":null,"parent_menu_id":null,"columns":[{"id":1,"uuid":"ed471acf-3ea2-410c-9751-ed5fd8b379bf","status":"0","description":null,"created_time":"2025-12-04 20:48:26","updated_time":"2025-12-04 20:48:26","table_id":1,"column_name":"name","column_comment":"名称","column_type":"varchar","column_length":"64","column_default":"","is_pk":false,"is_increment":false,"is_nullable":false,"is_unique":false,"python_type":"str","python_field":"name","is_insert":true,"is_edit":true,"is_list":true,"is_query":true,"query_type":"LIKE","html_type":"input","dict_type":"","sort":1,"super_column":"0"},{"id":2,"uuid":"9a4f7dd6-912d-498c-b438-1eda1fa3ba9c","status":"0","description":null,"created_time":"2025-12-04 20:48:26","updated_time":"2025-12-04 20:48:26","table_id":1,"column_name":"id","column_comment":"主键ID","column_type":"int4","column_length":"","column_default":"nextval('gen_demo_id_seq'::regclass)","is_pk":true,"is_increment":true,"is_nullable":true,"is_unique":false,"python_type":"int","python_field":"id","is_insert":true,"is_edit":false,"is_list":false,"is_query":false,"query_type":null,"html_type":"input","dict_type":"","sort":2,"super_column":"0"},{"id":3,"uuid":"ca6e8c47-fb53-48d6-8a96-223738f1341d","status":"0","description":null,"created_time":"2025-12-04 20:48:26","updated_time":"2025-12-04 20:48:26","table_id":1,"column_name":"uuid","column_comment":"UUID全局唯一标识","column_type":"varchar","column_length":"64","column_default":"","is_pk":false,"is_increment":false,"is_nullable":true,"is_unique":true,"python_type":"str","python_field":"uuid","is_insert":true,"is_edit":false,"is_list":false,"is_query":false,"query_type":null,"html_type":"input","dict_type":"","sort":3,"super_column":"0"},{"id":4,"uuid":"5ccd94c8-66cf-4828-a97f-bb22f4adcc03","status":"0","description":null,"created_time":"2025-12-04 20:48:26","updated_time":"2025-12-04 21:01:46","table_id":1,"column_name":"status","column_comment":"是否启用(0:启用 1:禁用)","column_type":"varchar","column_length":"10","column_default":"","is_pk":false,"is_increment":false,"is_nullable":true,"is_unique":false,"python_type":"str","python_field":"status","is_insert":true,"is_edit":true,"is_list":true,"is_query":true,"query_type":"EQ","html_type":"input","dict_type":"","sort":4,"super_column":"0"},{"id":5,"uuid":"cc66ab04-d191-496d-950d-1eb252c4dc5e","status":"0","description":null,"created_time":"2025-12-04 20:48:26","updated_time":"2025-12-04 20:48:26","table_id":1,"column_name":"description","column_comment":"备注/描述","column_type":"text","column_length":"","column_default":"","is_pk":false,"is_increment":false,"is_nullable":false,"is_unique":false,"python_type":"str","python_field":"description","is_insert":true,"is_edit":false,"is_list":false,"is_query":false,"query_type":null,"html_type":"input","dict_type":"","sort":5,"super_column":"0"},{"id":6,"uuid":"b59fc690-e38a-4467-ac7e-607761be32fd","status":"0","description":null,"created_time":"2025-12-04 20:48:26","updated_time":"2025-12-04 20:48:26","table_id":1,"column_name":"created_time","column_comment":"创建时间","column_type":"timestamp","column_length":"","column_default":"","is_pk":false,"is_increment":false,"is_nullable":true,"is_unique":false,"python_type":"datetime","python_field":"createdTime","is_insert":true,"is_edit":false,"is_list":false,"is_query":false,"query_type":null,"html_type":"input","dict_type":"","sort":6,"super_column":"0"},{"id":7,"uuid":"0437828b-9418-486b-9730-d80c80676a0f","status":"0","description":null,"created_time":"2025-12-04 20:48:26","updated_time":"2025-12-04 20:48:26","table_id":1,"column_name":"updated_time","column_comment":"更新时间","column_type":"timestamp","column_length":"","column_default":"","is_pk":false,"is_increment":false,"is_nullable":true,"is_unique":false,"python_type":"datetime","python_field":"updatedTime","is_insert":true,"is_edit":false,"is_list":false,"is_query":false,"query_type":null,"html_type":"input","dict_type":"","sort":7,"super_column":"0"},{"id":8,"uuid":"e2f84c36-fe6e-4800-ba85-39bb5c9232b8","status":"0","description":null,"created_time":"2025-12-04 20:48:26","updated_time":"2025-12-04 20:48:26","table_id":1,"column_name":"created_id","column_comment":"创建人ID","column_type":"int4","column_length":"","column_default":"","is_pk":false,"is_increment":false,"is_nullable":false,"is_unique":false,"python_type":"int","python_field":"createdId","is_insert":true,"is_edit":true,"is_list":true,"is_query":true,"query_type":"EQ","html_type":"input","dict_type":"","sort":8,"super_column":"0"},{"id":9,"uuid":"eaf874ef-be0b-44c3-828e-c35e8c3cdd76","status":"0","description":null,"created_time":"2025-12-04 20:48:26","updated_time":"2025-12-04 20:48:26","table_id":1,"column_name":"updated_id","column_comment":"更新人ID","column_type":"int4","column_length":"","column_default":"","is_pk":false,"is_increment":false,"is_nullable":false,"is_unique":false,"python_type":"int","python_field":"updatedId","is_insert":true,"is_edit":true,"is_list":true,"is_query":true,"query_type":"EQ","html_type":"input","dict_type":"","sort":9,"super_column":"0"}],"pk_column":null,"sub_table":null,"sub":null},"status_code":200,"success":true}	0.46s	5	6571b782-d579-42cf-89d8-92b005341a53	0	编辑业务表信息	2025-12-04 21:01:46.720077	2025-12-04 21:01:46.72008	1	1
2	/api/v1/generator/gencode/output/gen_demo	POST	{"path_params": {"table_name": "gen_demo"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"生成代码到指定路径成功","data":true,"status_code":200,"success":true}	0.11s	6	ec47c313-bb8f-4d0c-bf9c-354c3c20fe1b	0	生成代码到指定路径	2025-12-04 21:03:30.348878	2025-12-04 21:03:30.34888	1	1
2	/api/v1/system/dept/create	POST	{"body": {"name": "test1", "code": "test1", "order": 1, "parent_id": 1, "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建部门成功","data":{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},"status_code":200,"success":true}	0.06s	7	a763dd85-3677-4fe3-92dc-382482ca81f2	0	创建部门	2025-12-04 21:16:25.492703	2025-12-04 21:16:25.492707	1	1
2	/api/v1/system/dept/create	POST	{"body": {"name": "test2", "code": "test2", "order": 1, "parent_id": 1, "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建部门成功","data":{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},"status_code":200,"success":true}	0.03s	8	b383a314-d6e7-4936-876b-50a025da3fe0	0	创建部门	2025-12-04 21:16:35.828182	2025-12-04 21:16:35.828185	1	1
2	/api/v1/system/dept/create	POST	{"body": {"name": "test1_1", "code": "test1_1", "order": 1, "parent_id": 2, "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建部门成功","data":{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},"status_code":200,"success":true}	0.02s	9	952a12a4-c14d-41f4-b95e-3d0979313292	0	创建部门	2025-12-04 21:16:46.528317	2025-12-04 21:16:46.528319	1	1
2	/api/v1/system/dept/create	POST	{"body": {"name": "test1_2", "code": "test1_2", "order": 1, "parent_id": 2, "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建部门成功","data":{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},"status_code":200,"success":true}	0.02s	10	5d93ca3f-7087-42a9-9d19-642a48bbae34	0	创建部门	2025-12-04 21:17:23.732432	2025-12-04 21:17:23.732435	1	1
2	/api/v1/system/role/create	POST	{"body": {"name": "全部数据", "order": 1, "code": "ALL", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建角色成功","data":{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:23:11","name":"全部数据","code":"ALL","order":1,"data_scope":1,"menus":[],"depts":[]},"status_code":200,"success":true}	0.04s	14	c0dda3f6-5181-438e-8370-d5029a4527eb	0	创建角色	2025-12-04 21:23:11.233662	2025-12-04 21:23:11.233667	1	1
2	/api/v1/system/dept/create	POST	{"body": {"name": "test2_2", "code": "test2_2", "order": 1, "parent_id": 3, "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建部门成功","data":{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},"status_code":200,"success":true}	0.02s	11	7650697a-bd68-42c1-b5cb-5d7a87b6e580	0	创建部门	2025-12-04 21:17:36.045449	2025-12-04 21:17:36.045452	1	1
2	/api/v1/system/dept/create	POST	{"body": {"name": "test2_1", "code": "test2_1", "order": 1, "parent_id": 3, "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建部门成功","data":{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},"status_code":200,"success":true}	0.02s	12	aa848c76-fb46-40cb-8a5a-7e4b5a92d4ac	0	创建部门	2025-12-04 21:17:46.895661	2025-12-04 21:17:46.895663	1	1
2	/api/v1/system/role/create	POST	{"body": {"name": "仅个人数据", "order": 1, "code": "MINE", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建角色成功","data":{"id":2,"uuid":"242f44f5-6faf-4245-aac7-482630ddb6f7","status":"0","description":null,"created_time":"2025-12-04 21:22:35","updated_time":"2025-12-04 21:22:35","name":"仅个人数据","code":"MINE","order":1,"data_scope":1,"menus":[],"depts":[]},"status_code":200,"success":true}	0.06s	13	43e96a15-1371-4c5a-81d4-990a4d8424cb	0	创建角色	2025-12-04 21:22:35.121041	2025-12-04 21:22:35.121044	1	1
2	/api/v1/system/role/create	POST	{"body": {"name": "本部门数据", "order": 1, "code": "DEPT", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建角色成功","data":{"id":4,"uuid":"6a229f0d-7dcb-4b66-9054-987e3c1dfe5d","status":"0","description":null,"created_time":"2025-12-04 21:23:30","updated_time":"2025-12-04 21:23:30","name":"本部门数据","code":"DEPT","order":1,"data_scope":1,"menus":[],"depts":[]},"status_code":200,"success":true}	0.04s	15	c036e52d-4ca2-4dda-a314-f04fbf6d8985	0	创建角色	2025-12-04 21:23:30.480274	2025-12-04 21:23:30.480277	1	1
2	/api/v1/system/role/create	POST	{"body": {"name": "本部门及以下", "order": 1, "code": "ALL_DEPT", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建角色成功","data":{"id":5,"uuid":"b419c2ef-af62-4d93-80e5-4afb24be9289","status":"0","description":null,"created_time":"2025-12-04 21:23:50","updated_time":"2025-12-04 21:23:50","name":"本部门及以下","code":"ALL_DEPT","order":1,"data_scope":1,"menus":[],"depts":[]},"status_code":200,"success":true}	0.03s	16	b567200f-c48d-4569-bfbe-81d0ae893466	0	创建角色	2025-12-04 21:23:50.691965	2025-12-04 21:23:50.691969	1	1
2	/api/v1/system/role/permission/setting	PATCH	{"body": {"role_ids": [2], "menu_ids": [7, 29, 106, 107, 108, 109, 110, 111, 112], "data_scope": 1, "dept_ids": []}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"授权角色成功","data":null,"status_code":200,"success":true}	0.09s	17	eed6ed8c-663a-4196-9fe7-0b065751b17c	0	角色授权	2025-12-04 21:29:46.669168	2025-12-04 21:29:46.66917	1	1
2	/api/v1/system/role/permission/setting	PATCH	{"body": {"role_ids": [4], "menu_ids": [7, 29, 106, 107, 108, 109, 110, 111, 112], "data_scope": 2, "dept_ids": []}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"授权角色成功","data":null,"status_code":200,"success":true}	0.19s	18	d7e27634-0e25-4d07-a04f-3e959e4a86df	0	角色授权	2025-12-04 21:29:59.12125	2025-12-04 21:29:59.121253	1	1
2	/api/v1/system/role/permission/setting	PATCH	{"body": {"role_ids": [5], "menu_ids": [7, 29, 106, 107, 108, 109, 110, 111, 112], "data_scope": 3, "dept_ids": []}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"授权角色成功","data":null,"status_code":200,"success":true}	0.05s	19	64d446ee-33a8-4a10-ac74-b724864b4bae	0	角色授权	2025-12-04 21:30:14.541946	2025-12-04 21:30:14.541948	1	1
2	/api/v1/system/role/permission/setting	PATCH	{"body": {"role_ids": [3], "menu_ids": [7, 29, 106, 107, 108, 109, 110, 111, 112], "data_scope": 4, "dept_ids": []}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"授权角色成功","data":null,"status_code":200,"success":true}	0.05s	20	8a09655c-63cb-440a-80b9-079c1127d0cf	0	角色授权	2025-12-04 21:30:37.30874	2025-12-04 21:30:37.308743	1	1
2	/api/v1/system/role/create	POST	{"body": {"name": "自定义数据", "order": 1, "code": "ZIDINGYI", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建角色成功","data":{"id":6,"uuid":"96f6a404-d6b0-4a46-b6fa-5cbd56e42739","status":"0","description":null,"created_time":"2025-12-04 21:32:02","updated_time":"2025-12-04 21:32:02","name":"自定义数据","code":"ZIDINGYI","order":1,"data_scope":1,"menus":[],"depts":[]},"status_code":200,"success":true}	0.06s	21	2093bff2-cf51-40ca-a6df-00cc9f061a0d	0	创建角色	2025-12-04 21:32:02.727037	2025-12-04 21:32:02.727041	1	1
2	/api/v1/system/role/permission/setting	PATCH	{"body": {"role_ids": [6], "menu_ids": [7, 29, 106, 107, 108, 109, 110, 111, 112], "data_scope": 5, "dept_ids": [5]}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"授权角色成功","data":null,"status_code":200,"success":true}	0.05s	22	f629d2d3-6bdb-4671-a1e8-058bf979fd39	0	角色授权	2025-12-04 21:32:35.181681	2025-12-04 21:32:35.181683	1	1
2	/api/v1/system/user/reset/password	PUT	{"body": {"id": 2, "password": "123456"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"重置密码成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":2,"uuid":"3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29","status":"0","description":null,"created_time":"2025-12-03 23:24:32","updated_time":"2025-12-04 21:40:31","name":"test1","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1","password":"$2b$12$HZazPM6aOg2ZSy3a57qvR.6U7dn4FmuD6KST2.X3Os9D1s4w5iZQu","is_superuser":false,"dept_id":1,"role_ids":[],"position_ids":[],"last_login":null,"gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":1,"name":"集团总公司"},"positions":[],"roles":[{"id":1,"uuid":"f775fc7c-2643-4feb-a647-182f293b7952","status":"0","description":"初始化角色","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"管理员角色","code":"ADMIN","order":1,"data_scope":4,"menus":[],"depts":[]}],"menus":[]},"status_code":200,"success":true}	0.51s	23	dd6c2fb9-6a8a-4da9-bb04-b4cd13d7cf5d	0	重置密码	2025-12-04 21:40:31.170571	2025-12-04 21:40:31.170574	1	1
2	/api/v1/system/user/update/2	PUT	{"body": {"id": 2, "username": "test1", "name": "test1", "dept_id": 2, "dept_name": null, "role_ids": [3], "position_ids": [], "password": "$2b$12$HZazPM6aOg2ZSy3a57qvR.6U7dn4FmuD6KST2.X3Os9D1s4w5iZQu", "gender": "2", "email": null, "mobile": null, "is_superuser": false, "status": "0", "description": null, "created_id": 1, "created_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "updated_id": 1, "updated_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "uuid": "3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29", "created_time": "2025-12-03 23:24:32", "updated_time": "2025-12-04 21:40:31", "avatar": null, "last_login": null, "gitee_login": null, "github_login": null, "wx_login": null, "qq_login": null, "dept": {"id": 1, "name": "集团总公司"}, "positions": [], "roles": [{"id": 1, "uuid": "f775fc7c-2643-4feb-a647-182f293b7952", "status": "0", "description": "初始化角色", "created_time": "2025-12-03 23:23:58", "updated_time": "2025-12-03 23:23:58", "name": "管理员角色", "code": "ADMIN", "order": 1, "data_scope": 4, "menus": [], "depts": []}], "menus": []}, "path_params": {"id": "2"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":2,"uuid":"3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29","status":"0","description":null,"created_time":"2025-12-03 23:24:32","updated_time":"2025-12-04 21:40:47","name":"test1","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1","password":"$2b$12$gn.WYUQfWX9NF9MgK/QabuieVJbb5NP2ceuL/AENhze0FQWM7Q8zy","is_superuser":false,"dept_id":2,"role_ids":[],"position_ids":[],"last_login":null,"gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":2,"name":"test1"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.45s	24	b1bd6b42-3c68-41d2-b033-b3aae0572eb2	0	修改用户	2025-12-04 21:40:47.653518	2025-12-04 21:40:47.653521	1	1
2	/api/v1/system/user/reset/password	PUT	{"body": {"id": 2, "password": "123456"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"重置密码成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":2,"uuid":"3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29","status":"0","description":null,"created_time":"2025-12-03 23:24:32","updated_time":"2025-12-04 21:40:54","name":"test1","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1","password":"$2b$12$akRj6sW1qG4pNP2dqpn58O6bYIK/57K0vqJ4B76puts61qOwsjmwu","is_superuser":false,"dept_id":2,"role_ids":[],"position_ids":[],"last_login":null,"gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":2,"name":"test1"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.35s	25	db7598ee-1750-4820-9537-f933330315ff	0	重置密码	2025-12-04 21:40:54.948684	2025-12-04 21:40:54.948686	1	1
2	/api/v1/system/user/create	POST	{"body": {"username": "test2", "name": "test2", "dept_id": 3, "role_ids": [3], "password": "123456", "is_superuser": false, "status": "0", "created_id": 1, "created_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "updated_id": 1, "updated_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "uuid": "3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29", "created_time": "2025-12-03 23:24:32", "updated_time": "2025-12-04 21:40:31", "avatar": null, "last_login": null, "gitee_login": null, "github_login": null, "wx_login": null, "qq_login": null, "dept": {"id": 1, "name": "集团总公司"}, "positions": [], "roles": [{"id": 1, "uuid": "f775fc7c-2643-4feb-a647-182f293b7952", "status": "0", "description": "初始化角色", "created_time": "2025-12-03 23:23:58", "updated_time": "2025-12-03 23:23:58", "name": "管理员角色", "code": "ADMIN", "order": 1, "data_scope": 4, "menus": [], "depts": []}], "menus": []}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":3,"uuid":"4c2b0473-3130-4c4d-bebf-94412ea05c7e","status":"0","description":null,"created_time":"2025-12-04 21:41:18","updated_time":"2025-12-04 21:41:18","name":"test2","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2","password":"$2b$12$J4CW15v/OXHFP9YLdgfeyORJ0krN61G3icmj.EwQPMXzPRsTM56Uq","is_superuser":false,"dept_id":3,"role_ids":[],"position_ids":[],"last_login":null,"gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":3,"name":"test2"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.33s	26	b657d505-a4aa-4040-9abd-210c47ef2212	0	创建用户	2025-12-04 21:41:18.609037	2025-12-04 21:41:18.60904	1	1
2	/api/v1/gencode/demo/create	POST	{"body": {"name": "test1", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建示例成功","data":{"created_id":2,"created_by":{"id":2,"name":"test1","username":"test1"},"updated_id":2,"updated_by":{"id":2,"name":"test1","username":"test1"},"id":3,"uuid":"7f0e50b5-ed5f-41c0-b6c1-a89e9bf1c33b","status":"0","description":null,"created_time":"2025-12-04 21:47:23","updated_time":"2025-12-04 21:47:23","name":"test1"},"status_code":200,"success":true}	0.05s	35	b2f0a3cb-f3e6-4a1c-bcec-13e02ce9e258	0	创建示例	2025-12-04 21:47:23.98283	2025-12-04 21:47:23.982833	2	2
2	/api/v1/system/user/create	POST	{"body": {"username": "test1_1", "name": "test1_1", "dept_id": 4, "role_ids": [3], "password": "123456", "is_superuser": false, "status": "0", "created_id": 1, "created_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "updated_id": 1, "updated_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "uuid": "3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29", "created_time": "2025-12-03 23:24:32", "updated_time": "2025-12-04 21:40:31", "avatar": null, "last_login": null, "gitee_login": null, "github_login": null, "wx_login": null, "qq_login": null, "dept": {"id": 1, "name": "集团总公司"}, "positions": [], "roles": [{"id": 1, "uuid": "f775fc7c-2643-4feb-a647-182f293b7952", "status": "0", "description": "初始化角色", "created_time": "2025-12-03 23:23:58", "updated_time": "2025-12-03 23:23:58", "name": "管理员角色", "code": "ADMIN", "order": 1, "data_scope": 4, "menus": [], "depts": []}], "menus": []}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":4,"uuid":"0164b4be-69e8-437e-9b37-87727eae3964","status":"0","description":null,"created_time":"2025-12-04 21:41:51","updated_time":"2025-12-04 21:41:51","name":"test1_1","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1_1","password":"$2b$12$XoZkF1kKghOsh8uUVumkse4iI48DfkN1Fz6NTdHWMg3OfaAp71C8i","is_superuser":false,"dept_id":4,"role_ids":[],"position_ids":[],"last_login":null,"gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":4,"name":"test1_1"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.31s	27	19660f76-0e9a-4c6d-9e28-8499fd7f7c6d	0	创建用户	2025-12-04 21:41:51.196461	2025-12-04 21:41:51.196465	1	1
2	/api/v1/system/user/create	POST	{"body": {"username": "test1_2", "name": "test1_2", "dept_id": 5, "role_ids": [3], "password": "123456", "is_superuser": false, "status": "0", "created_id": 1, "created_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "updated_id": 1, "updated_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "uuid": "3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29", "created_time": "2025-12-03 23:24:32", "updated_time": "2025-12-04 21:40:31", "avatar": null, "last_login": null, "gitee_login": null, "github_login": null, "wx_login": null, "qq_login": null, "dept": {"id": 1, "name": "集团总公司"}, "positions": [], "roles": [{"id": 1, "uuid": "f775fc7c-2643-4feb-a647-182f293b7952", "status": "0", "description": "初始化角色", "created_time": "2025-12-03 23:23:58", "updated_time": "2025-12-03 23:23:58", "name": "管理员角色", "code": "ADMIN", "order": 1, "data_scope": 4, "menus": [], "depts": []}], "menus": []}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":5,"uuid":"b730fcb1-2cff-472c-9809-a4167313e6fb","status":"0","description":null,"created_time":"2025-12-04 21:44:44","updated_time":"2025-12-04 21:44:44","name":"test1_2","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1_2","password":"$2b$12$Bz5XlxBQQ7FzYSLuSMSfle7iR3vBH/hn46LZR.IFzn04lqG7eR7DO","is_superuser":false,"dept_id":5,"role_ids":[],"position_ids":[],"last_login":null,"gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":5,"name":"test1_2"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.33s	28	aa32fe05-2936-4cbb-877e-f2fe72ffe339	0	创建用户	2025-12-04 21:44:44.286166	2025-12-04 21:44:44.286168	1	1
2	/api/v1/system/user/create	POST	{"body": {"username": "test2_1", "name": "test2_1", "dept_id": 7, "role_ids": [3], "password": "123456", "is_superuser": false, "status": "0", "created_id": 1, "created_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "updated_id": 1, "updated_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "uuid": "3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29", "created_time": "2025-12-03 23:24:32", "updated_time": "2025-12-04 21:40:31", "avatar": null, "last_login": null, "gitee_login": null, "github_login": null, "wx_login": null, "qq_login": null, "dept": {"id": 1, "name": "集团总公司"}, "positions": [], "roles": [{"id": 1, "uuid": "f775fc7c-2643-4feb-a647-182f293b7952", "status": "0", "description": "初始化角色", "created_time": "2025-12-03 23:23:58", "updated_time": "2025-12-03 23:23:58", "name": "管理员角色", "code": "ADMIN", "order": 1, "data_scope": 4, "menus": [], "depts": []}], "menus": []}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":6,"uuid":"46f2a531-af05-423f-a504-cee642327336","status":"0","description":null,"created_time":"2025-12-04 21:46:20","updated_time":"2025-12-04 21:46:20","name":"test2_1","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2_1","password":"$2b$12$I82W2vdZeAZ9LKy077xHgO8EvjdiyKKMY7K.GcCeY/Xy7QefheKZm","is_superuser":false,"dept_id":7,"role_ids":[],"position_ids":[],"last_login":null,"gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":7,"name":"test2_1"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.33s	29	9c8342cd-d813-40c7-80d8-967d3382cb9b	0	创建用户	2025-12-04 21:46:20.560803	2025-12-04 21:46:20.560806	1	1
2	/api/v1/system/user/create	POST	{"body": {"username": "test2_2", "name": "test2_2", "dept_id": 6, "role_ids": [3], "password": "123456", "is_superuser": false, "status": "0", "created_id": 1, "created_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "updated_id": 1, "updated_by": {"id": 1, "name": "超级管理员", "username": "admin"}, "uuid": "3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29", "created_time": "2025-12-03 23:24:32", "updated_time": "2025-12-04 21:40:31", "avatar": null, "last_login": null, "gitee_login": null, "github_login": null, "wx_login": null, "qq_login": null, "dept": {"id": 1, "name": "集团总公司"}, "positions": [], "roles": [{"id": 1, "uuid": "f775fc7c-2643-4feb-a647-182f293b7952", "status": "0", "description": "初始化角色", "created_time": "2025-12-03 23:23:58", "updated_time": "2025-12-03 23:23:58", "name": "管理员角色", "code": "ADMIN", "order": 1, "data_scope": 4, "menus": [], "depts": []}], "menus": []}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":7,"uuid":"da0c4cec-c428-4347-ba67-ec6b1878fc2c","status":"0","description":null,"created_time":"2025-12-04 21:46:42","updated_time":"2025-12-04 21:46:42","name":"test2_2","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2_2","password":"$2b$12$lmd185zT9n2CsfLvta33rOqeLixCFrounwK1dwTFJqZ.tQmu6D0.m","is_superuser":false,"dept_id":6,"role_ids":[],"position_ids":[],"last_login":null,"gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":6,"name":"test2_2"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.41s	30	1e465514-c30c-4123-891b-29d94c6daa08	0	创建用户	2025-12-04 21:46:43.010872	2025-12-04 21:46:43.010875	1	1
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcImY0YTFlZDhiLWFhNmEtNDI3ZC1iMzYxLTk0ZGFjNDMxMTc5NlwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDMgMTQ6MzY6MzRcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc2OTk4NTM5NH0.52eHi56_lvZYT7LaWI6Xa5Hua3WNteCTgBgHE4fxOj8"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.03s	31	edb02766-d92c-4140-a650-304d7672515e	0	退出登录	2025-12-04 21:46:50.789402	2025-12-04 21:46:50.789404	1	1
1	/api/v1/system/auth/login	POST	username: test1\npassword: 123456\ncaptcha: 5\ncaptcha_key: 0ce1bbd218d0493ea2ac3aa15b828720\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MVwiLFwic2Vzc2lvbl9pZFwiOlwiYjlkNTNlZWYtOWQzMS00NjQ0LTkxZTQtODcxY2YyZDYwY2M3XCIsXCJ1c2VyX2lkXCI6MixcInVzZXJfbmFtZVwiOlwidGVzdDFcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxMzo0NzowMFwiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjpmYWxzZSwiZXhwIjoxNzcwMDY4ODIwfQ.vhTuHoGvc5DvtIcEPqmrc6Pp3uDN3Tsj-wvAwwzH2sY","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MVwiLFwic2Vzc2lvbl9pZFwiOlwiYjlkNTNlZWYtOWQzMS00NjQ0LTkxZTQtODcxY2YyZDYwY2M3XCIsXCJ1c2VyX2lkXCI6MixcInVzZXJfbmFtZVwiOlwidGVzdDFcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxMzo0NzowMFwiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjp0cnVlLCJleHAiOjE4MDExNzI4MjB9.JmsaiPByupfp6DQVBn4ugunYCoiMzAWtDV1i4BB5mwY","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.41s	32	d3527dfc-1bd6-4e5a-988b-4fb6f3b06295	0	登录	2025-12-04 21:47:00.696208	2025-12-04 21:47:00.696211	\N	\N
2	/api/v1/gencode/demo/delete	DELETE	{"body": [1]}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"删除示例成功","data":null,"status_code":200,"success":true}	0.14s	33	bc869e82-c91b-413e-b838-b52fb07dff73	0	删除示例	2025-12-04 21:47:14.097738	2025-12-04 21:47:14.097741	2	2
2	/api/v1/gencode/demo/delete	DELETE	{"body": [2]}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"删除示例成功","data":null,"status_code":200,"success":true}	0.07s	34	23d333f7-a96d-4279-8db2-9845f610eae8	0	删除示例	2025-12-04 21:47:16.469362	2025-12-04 21:47:16.469364	2	2
2	/api/v1/system/user/create	POST	{"body": {"username": "test22", "name": "本部门数据2", "dept_id": 3, "role_ids": [4], "password": "123456", "is_superuser": false, "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":8,"uuid":"795f3692-ad0c-44ea-8e36-4bcb6c4dd957","status":"0","description":null,"created_time":"2025-12-04 22:06:19","updated_time":"2025-12-04 22:06:19","name":"本部门数据2","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test22","password":"$2b$12$/0pNNfFW1n3dEJAnPxe6LOmodfU1zHbPmUGsNPOW1ucOOOUbEAHVm","is_superuser":false,"dept_id":3,"role_ids":[],"position_ids":[],"last_login":null,"gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":3,"name":"test2"},"positions":[],"roles":[{"id":4,"uuid":"6a229f0d-7dcb-4b66-9054-987e3c1dfe5d","status":"0","description":null,"created_time":"2025-12-04 21:23:30","updated_time":"2025-12-04 21:29:59","name":"本部门数据","code":"DEPT","order":1,"data_scope":2,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.37s	85	9fd06978-bff8-42ed-a17e-b5b498848d77	0	创建用户	2025-12-04 22:06:19.341551	2025-12-04 22:06:19.341554	1	1
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MVwiLFwic2Vzc2lvbl9pZFwiOlwiYjlkNTNlZWYtOWQzMS00NjQ0LTkxZTQtODcxY2YyZDYwY2M3XCIsXCJ1c2VyX2lkXCI6MixcInVzZXJfbmFtZVwiOlwidGVzdDFcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxMzo0NzowMFwiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjpmYWxzZSwiZXhwIjoxNzcwMDY4ODIwfQ.vhTuHoGvc5DvtIcEPqmrc6Pp3uDN3Tsj-wvAwwzH2sY"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.05s	36	843f5e57-ad60-4436-a470-2ec3472e557a	0	退出登录	2025-12-04 21:47:29.05841	2025-12-04 21:47:29.058425	2	2
1	/api/v1/system/auth/login	POST	username: test2\npassword: 123456\ncaptcha: 12\ncaptcha_key: 4f4e4d81414d4a819317e7885b686209\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MlwiLFwic2Vzc2lvbl9pZFwiOlwiYWU0NzI3NWMtYWMyNy00MjYwLWJkMGEtZGFhODg2YjcxOGZlXCIsXCJ1c2VyX2lkXCI6MyxcInVzZXJfbmFtZVwiOlwidGVzdDJcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxMzo0NzozN1wiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjpmYWxzZSwiZXhwIjoxNzcwMDY4ODU3fQ.1o_2cC0oIJX89Wk8m5JWYDZ2sIYP0N3fm3MAKeb33wU","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MlwiLFwic2Vzc2lvbl9pZFwiOlwiYWU0NzI3NWMtYWMyNy00MjYwLWJkMGEtZGFhODg2YjcxOGZlXCIsXCJ1c2VyX2lkXCI6MyxcInVzZXJfbmFtZVwiOlwidGVzdDJcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxMzo0NzozN1wiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjp0cnVlLCJleHAiOjE4MDExNzI4NTd9.S0P90BfakMTC01dYHt_d8Cu2nQEyONOJ1nPl0aUSXP0","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.35s	37	a1b58771-98f7-4746-8214-f98c57164699	0	登录	2025-12-04 21:47:37.272474	2025-12-04 21:47:37.272475	\N	\N
2	/api/v1/gencode/demo/create	POST	{"body": {"name": "test2", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建示例成功","data":{"created_id":3,"created_by":{"id":3,"name":"test2","username":"test2"},"updated_id":3,"updated_by":{"id":3,"name":"test2","username":"test2"},"id":4,"uuid":"165c3e41-d9e8-4dcf-b5ad-ca393bb13c38","status":"0","description":null,"created_time":"2025-12-04 21:47:47","updated_time":"2025-12-04 21:47:47","name":"test2"},"status_code":200,"success":true}	0.05s	38	f74b7678-2a1b-4cfd-8255-a2862c403c82	0	创建示例	2025-12-04 21:47:47.310965	2025-12-04 21:47:47.310968	3	3
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MlwiLFwic2Vzc2lvbl9pZFwiOlwiYWU0NzI3NWMtYWMyNy00MjYwLWJkMGEtZGFhODg2YjcxOGZlXCIsXCJ1c2VyX2lkXCI6MyxcInVzZXJfbmFtZVwiOlwidGVzdDJcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxMzo0NzozN1wiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjpmYWxzZSwiZXhwIjoxNzcwMDY4ODU3fQ.1o_2cC0oIJX89Wk8m5JWYDZ2sIYP0N3fm3MAKeb33wU"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.11s	39	eb54feff-90db-4742-93d0-79b8b865ec5a	0	退出登录	2025-12-04 21:47:53.149231	2025-12-04 21:47:53.149234	3	3
1	/api/v1/system/auth/login	POST	username: admin\npassword: 123456\ncaptcha: 54\ncaptcha_key: 95fc2aa574904a30beb2ba4d36042c15\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjE5MDJiNjgzLTI0YzYtNDAzNi04ZjcyLTA0NzQwNjQyNWMyZFwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NDg6MDJcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2ODg4Mn0.rUfkhVurokfK8beaFd9G0rrbD0y4qMnjK7Il4oo89mc","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjE5MDJiNjgzLTI0YzYtNDAzNi04ZjcyLTA0NzQwNjQyNWMyZFwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NDg6MDJcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTcyODgyfQ.kbVvRZT_KrEXzPYRH2AhMXNVO1FuYAoy6gpw0vt6aN4","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.32s	40	6603e655-0f6a-4837-98d5-c09f91f256ab	0	登录	2025-12-04 21:48:02.593539	2025-12-04 21:48:02.59354	\N	\N
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjE5MDJiNjgzLTI0YzYtNDAzNi04ZjcyLTA0NzQwNjQyNWMyZFwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NDg6MDJcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2ODg4Mn0.rUfkhVurokfK8beaFd9G0rrbD0y4qMnjK7Il4oo89mc"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.02s	41	db5008d6-7279-4817-8325-9640894613f2	0	退出登录	2025-12-04 21:48:18.903191	2025-12-04 21:48:18.903194	1	1
1	/api/v1/system/auth/login	POST	username: test1_1\npassword: 123456\ncaptcha: 5\ncaptcha_key: 7790d6f3cf0541788bd494581647d7a8\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MV8xXCIsXCJzZXNzaW9uX2lkXCI6XCI5OWFjNThlNy0xYWY1LTRiN2UtOWY1ZS04M2NkMGFmN2FjOGVcIixcInVzZXJfaWRcIjo0LFwidXNlcl9uYW1lXCI6XCJ0ZXN0MV8xXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NDg6MjZcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2ODkwNn0.Q4jhiKcrC21ScXEFSHUlHjtTQjVCI8sUF6VPgcI0N5I","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MV8xXCIsXCJzZXNzaW9uX2lkXCI6XCI5OWFjNThlNy0xYWY1LTRiN2UtOWY1ZS04M2NkMGFmN2FjOGVcIixcInVzZXJfaWRcIjo0LFwidXNlcl9uYW1lXCI6XCJ0ZXN0MV8xXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NDg6MjZcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTcyOTA2fQ.Ug7LmD5eekiIk0VXJkOcVBD-a2MXc5Al5ixNqFyLYeo","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.37s	42	06af859b-e0ce-41da-8971-ff0d58c1126d	0	登录	2025-12-04 21:48:26.651428	2025-12-04 21:48:26.65143	\N	\N
2	/api/v1/gencode/demo/create	POST	{"body": {"name": "test101", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建示例成功","data":{"created_id":4,"created_by":{"id":4,"name":"test1_1","username":"test1_1"},"updated_id":4,"updated_by":{"id":4,"name":"test1_1","username":"test1_1"},"id":5,"uuid":"2d02f458-3b78-4e6b-a619-403b406d21f6","status":"0","description":null,"created_time":"2025-12-04 21:49:09","updated_time":"2025-12-04 21:49:09","name":"test101"},"status_code":200,"success":true}	0.06s	43	a2cac2e3-bba4-45c6-b9a4-75e346c282c3	0	创建示例	2025-12-04 21:49:09.241275	2025-12-04 21:49:09.24128	4	4
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MV8xXCIsXCJzZXNzaW9uX2lkXCI6XCI5OWFjNThlNy0xYWY1LTRiN2UtOWY1ZS04M2NkMGFmN2FjOGVcIixcInVzZXJfaWRcIjo0LFwidXNlcl9uYW1lXCI6XCJ0ZXN0MV8xXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NDg6MjZcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2ODkwNn0.Q4jhiKcrC21ScXEFSHUlHjtTQjVCI8sUF6VPgcI0N5I"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.06s	44	21863ed1-1e5b-40a2-8aea-572c86c15e4b	0	退出登录	2025-12-04 21:49:15.651918	2025-12-04 21:49:15.651921	4	4
1	/api/v1/system/auth/login	POST	username: test1_2\npassword: 123456\ncaptcha: 4\ncaptcha_key: 0f5c0189446043bb98cb3bc552394d63\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MV8yXCIsXCJzZXNzaW9uX2lkXCI6XCI2Mzg1ZjcyOS0wMmQzLTQwMGEtOTM3Zi1kM2MwMDI2ODIyMDBcIixcInVzZXJfaWRcIjo1LFwidXNlcl9uYW1lXCI6XCJ0ZXN0MV8yXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NDk6MjRcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2ODk2NH0.uzcIsT1lsYoAjOF-y_R5042PxcHbqgSFQcq9qNK2-bA","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MV8yXCIsXCJzZXNzaW9uX2lkXCI6XCI2Mzg1ZjcyOS0wMmQzLTQwMGEtOTM3Zi1kM2MwMDI2ODIyMDBcIixcInVzZXJfaWRcIjo1LFwidXNlcl9uYW1lXCI6XCJ0ZXN0MV8yXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NDk6MjRcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTcyOTY0fQ.CreFJrFQepC1E84oK0fAsirXHv-OSaxuQVRtAT08atk","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.36s	45	55747dc9-b08b-420a-8cb4-a71977d3e0d4	0	登录	2025-12-04 21:49:24.102945	2025-12-04 21:49:24.102947	\N	\N
2	/api/v1/gencode/demo/create	POST	{"body": {"name": "test102", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建示例成功","data":{"created_id":5,"created_by":{"id":5,"name":"test1_2","username":"test1_2"},"updated_id":5,"updated_by":{"id":5,"name":"test1_2","username":"test1_2"},"id":6,"uuid":"82437f97-65c0-4c9f-8d49-822e1e3010e9","status":"0","description":null,"created_time":"2025-12-04 21:49:39","updated_time":"2025-12-04 21:49:39","name":"test102"},"status_code":200,"success":true}	0.05s	46	d75efc27-cf0f-49a3-ac7c-e0042b616bb1	0	创建示例	2025-12-04 21:49:39.165303	2025-12-04 21:49:39.165306	5	5
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0MV8yXCIsXCJzZXNzaW9uX2lkXCI6XCI2Mzg1ZjcyOS0wMmQzLTQwMGEtOTM3Zi1kM2MwMDI2ODIyMDBcIixcInVzZXJfaWRcIjo1LFwidXNlcl9uYW1lXCI6XCJ0ZXN0MV8yXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NDk6MjRcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2ODk2NH0.uzcIsT1lsYoAjOF-y_R5042PxcHbqgSFQcq9qNK2-bA"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.11s	47	cdb1fcd5-42d5-438c-b908-144739ab51e1	0	退出登录	2025-12-04 21:49:51.551167	2025-12-04 21:49:51.55117	5	5
1	/api/v1/system/auth/login	POST	username: test2_1\npassword: 123456\ncaptcha: 14\ncaptcha_key: f79f0693646b4243bef28d4efe3b333d\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0Ml8xXCIsXCJzZXNzaW9uX2lkXCI6XCJiZjRlMDJmZi0wNWVkLTRlMTktYjljYy04MmJlZGNiZGRlYjdcIixcInVzZXJfaWRcIjo2LFwidXNlcl9uYW1lXCI6XCJ0ZXN0Ml8xXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTA6MDFcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTAwMX0.f-9jgxcefzidrLC66O04eLawnodxSDeWy8Vnz6qEqYE","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0Ml8xXCIsXCJzZXNzaW9uX2lkXCI6XCJiZjRlMDJmZi0wNWVkLTRlMTktYjljYy04MmJlZGNiZGRlYjdcIixcInVzZXJfaWRcIjo2LFwidXNlcl9uYW1lXCI6XCJ0ZXN0Ml8xXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTA6MDFcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTczMDAxfQ.m3WqA_NKMa-YX79pVmdi4v4ro7RIvcczQ8pvmW5zYRk","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.37s	48	846f148b-e96d-4035-8002-c1c746c54fd8	0	登录	2025-12-04 21:50:01.797413	2025-12-04 21:50:01.797414	\N	\N
2	/api/v1/gencode/demo/create	POST	{"body": {"name": "test201", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建示例成功","data":{"created_id":6,"created_by":{"id":6,"name":"test2_1","username":"test2_1"},"updated_id":6,"updated_by":{"id":6,"name":"test2_1","username":"test2_1"},"id":7,"uuid":"b450605a-354c-4345-ae9c-4296454da490","status":"0","description":null,"created_time":"2025-12-04 21:50:19","updated_time":"2025-12-04 21:50:19","name":"test201"},"status_code":200,"success":true}	0.06s	49	11412102-d69a-4421-8272-710989f5ac0f	0	创建示例	2025-12-04 21:50:19.014998	2025-12-04 21:50:19.015001	6	6
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0Ml8xXCIsXCJzZXNzaW9uX2lkXCI6XCJiZjRlMDJmZi0wNWVkLTRlMTktYjljYy04MmJlZGNiZGRlYjdcIixcInVzZXJfaWRcIjo2LFwidXNlcl9uYW1lXCI6XCJ0ZXN0Ml8xXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTA6MDFcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTAwMX0.f-9jgxcefzidrLC66O04eLawnodxSDeWy8Vnz6qEqYE"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.04s	50	0706ea9b-0af6-4073-ac0b-01aab7b0efbd	0	退出登录	2025-12-04 21:50:25.249621	2025-12-04 21:50:25.249623	6	6
1	/api/v1/system/auth/login	POST	username: test2_2\npassword: 123456\ncaptcha: 11\ncaptcha_key: 312109b36ac241dd98c386ddb33f6226\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0Ml8yXCIsXCJzZXNzaW9uX2lkXCI6XCI5YTY3MGY3Ny1jNTdmLTQ5MjgtOTIzOS04NTVlY2Y2MDI3ZTJcIixcInVzZXJfaWRcIjo3LFwidXNlcl9uYW1lXCI6XCJ0ZXN0Ml8yXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTA6MzZcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTAzNn0.5U2ARspgghnE4Dd_7ehdTeu3xJB_AMCC_0XcaV4mN1U","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0Ml8yXCIsXCJzZXNzaW9uX2lkXCI6XCI5YTY3MGY3Ny1jNTdmLTQ5MjgtOTIzOS04NTVlY2Y2MDI3ZTJcIixcInVzZXJfaWRcIjo3LFwidXNlcl9uYW1lXCI6XCJ0ZXN0Ml8yXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTA6MzZcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTczMDM2fQ.HR7EqqgrViRGfED44XKFRGwx8xpUXfg2Cz1GvtPPmoA","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.36s	51	a442b273-d710-4fdc-9c4b-99c425071608	0	登录	2025-12-04 21:50:36.156628	2025-12-04 21:50:36.15663	\N	\N
2	/api/v1/gencode/demo/create	POST	{"body": {"name": "test202", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建示例成功","data":{"created_id":7,"created_by":{"id":7,"name":"test2_2","username":"test2_2"},"updated_id":7,"updated_by":{"id":7,"name":"test2_2","username":"test2_2"},"id":8,"uuid":"6a340642-aca6-478a-9b8b-16b7f238e16c","status":"0","description":null,"created_time":"2025-12-04 21:50:50","updated_time":"2025-12-04 21:50:50","name":"test202"},"status_code":200,"success":true}	0.05s	52	4113d68f-8a8b-4fde-99f6-370e48630c36	0	创建示例	2025-12-04 21:50:50.110721	2025-12-04 21:50:50.110723	7	7
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJ0ZXN0Ml8yXCIsXCJzZXNzaW9uX2lkXCI6XCI5YTY3MGY3Ny1jNTdmLTQ5MjgtOTIzOS04NTVlY2Y2MDI3ZTJcIixcInVzZXJfaWRcIjo3LFwidXNlcl9uYW1lXCI6XCJ0ZXN0Ml8yXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTA6MzZcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTAzNn0.5U2ARspgghnE4Dd_7ehdTeu3xJB_AMCC_0XcaV4mN1U"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.05s	53	65fc50c9-68bb-4d63-ac5b-5ed5b7735fb3	0	退出登录	2025-12-04 21:51:06.52789	2025-12-04 21:51:06.527893	7	7
1	/api/v1/system/auth/login	POST	username: admin\npassword: 123456\ncaptcha: 10\ncaptcha_key: 910c7f2fabed4ddc927e53d3ca41ac2d\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjY4YjZiY2JjLTU5ODItNGI4ZC1iMTlhLWIzMDEwOTg4ODFkM1wiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTE6MTFcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTA3MX0.SjvHPXMlw2GowjGWP8HN7hQiIgWCLR7Oy0Kpchk_zys","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjY4YjZiY2JjLTU5ODItNGI4ZC1iMTlhLWIzMDEwOTg4ODFkM1wiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTE6MTFcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTczMDcxfQ.FjNZ4t67G7HocpRacUOAsV6ypWIvLhMMkK1wMN0Lpd0","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.33s	54	7e239c11-92b5-493c-8445-3bf54c0c9a94	0	登录	2025-12-04 21:51:11.349045	2025-12-04 21:51:11.349047	\N	\N
2	/api/v1/system/user/update/3	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":3,"uuid":"4c2b0473-3130-4c4d-bebf-94412ea05c7e","status":"0","description":null,"created_time":"2025-12-04 21:41:18","updated_time":"2025-12-04 21:52:23","name":"test2","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2","password":"$2b$12$xxPwKicABhRAuiJU.neSzOY0PSiICk5furaZQFt4GgJlgjj2lDeHq","is_superuser":false,"dept_id":3,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:47:37","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":3,"name":"test2"},"positions":[],"roles":[{"id":4,"uuid":"6a229f0d-7dcb-4b66-9054-987e3c1dfe5d","status":"0","description":null,"created_time":"2025-12-04 21:23:30","updated_time":"2025-12-04 21:29:59","name":"本部门数据","code":"DEPT","order":1,"data_scope":2,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.45s	55	0fb1c74b-c93c-4a3d-bd39-e50fac166f58	0	修改用户	2025-12-04 21:52:23.486735	2025-12-04 21:52:23.486737	1	1
2	/api/v1/system/user/update/3	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":3,"uuid":"4c2b0473-3130-4c4d-bebf-94412ea05c7e","status":"0","description":null,"created_time":"2025-12-04 21:41:18","updated_time":"2025-12-04 21:52:52","name":"本部门数据","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2","password":"$2b$12$WvoRI/AmXl.gdvcP.GE9BuRTYYHpQIhFXZ2NTYi6z/3TUCNvZJ0Ou","is_superuser":false,"dept_id":3,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:47:37","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":3,"name":"test2"},"positions":[],"roles":[{"id":4,"uuid":"6a229f0d-7dcb-4b66-9054-987e3c1dfe5d","status":"0","description":null,"created_time":"2025-12-04 21:23:30","updated_time":"2025-12-04 21:29:59","name":"本部门数据","code":"DEPT","order":1,"data_scope":2,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.45s	56	0ca52a4e-4201-45c4-bd60-f0373c0274e8	0	修改用户	2025-12-04 21:52:52.147187	2025-12-04 21:52:52.14719	1	1
2	/api/v1/system/user/update/2	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":2,"uuid":"3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29","status":"0","description":null,"created_time":"2025-12-03 23:24:32","updated_time":"2025-12-04 21:53:21","name":"本部门及以下","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1","password":"$2b$12$zNj1mG8Kwfc83TP78lpXPOp4WKILKMEk30fdlW/n7nPfd.C7lAth.","is_superuser":false,"dept_id":2,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:47:00","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":2,"name":"test1"},"positions":[],"roles":[{"id":5,"uuid":"b419c2ef-af62-4d93-80e5-4afb24be9289","status":"0","description":null,"created_time":"2025-12-04 21:23:50","updated_time":"2025-12-04 21:30:14","name":"本部门及以下","code":"ALL_DEPT","order":1,"data_scope":3,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.44s	57	24ff50cb-e471-4050-8191-1faaf6e30b3b	0	修改用户	2025-12-04 21:53:21.820549	2025-12-04 21:53:21.820551	1	1
2	/api/v1/system/user/update/5	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":5,"uuid":"b730fcb1-2cff-472c-9809-a4167313e6fb","status":"0","description":null,"created_time":"2025-12-04 21:44:44","updated_time":"2025-12-04 21:54:05","name":"test1_2","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1_2","password":"$2b$12$SDKygdnC.zRYOsWkISOBye/Nu82FJnBzjZlV5AQKFFkpIoIeigqMK","is_superuser":false,"dept_id":5,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:49:24","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":5,"name":"test1_2"},"positions":[],"roles":[{"id":2,"uuid":"242f44f5-6faf-4245-aac7-482630ddb6f7","status":"0","description":null,"created_time":"2025-12-04 21:22:35","updated_time":"2025-12-04 21:29:46","name":"仅个人数据","code":"MINE","order":1,"data_scope":1,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.44s	58	ff3688f7-ca00-46dd-99c6-276a2119e281	0	修改用户	2025-12-04 21:54:05.162402	2025-12-04 21:54:05.162407	1	1
2	/api/v1/system/user/update/5	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":5,"uuid":"b730fcb1-2cff-472c-9809-a4167313e6fb","status":"0","description":null,"created_time":"2025-12-04 21:44:44","updated_time":"2025-12-04 21:54:15","name":"仅个人","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1_2","password":"$2b$12$AcDzjk74xdQwfQFf2rbAeeFhmqezt6xetRBalsgJEqMd8pcJcZ/s6","is_superuser":false,"dept_id":5,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:49:24","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":5,"name":"test1_2"},"positions":[],"roles":[{"id":2,"uuid":"242f44f5-6faf-4245-aac7-482630ddb6f7","status":"0","description":null,"created_time":"2025-12-04 21:22:35","updated_time":"2025-12-04 21:29:46","name":"仅个人数据","code":"MINE","order":1,"data_scope":1,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.46s	59	a0536b5f-d1d3-4e09-a273-5c273494784f	0	修改用户	2025-12-04 21:54:15.193675	2025-12-04 21:54:15.193677	1	1
2	/api/v1/system/user/update/6	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":6,"uuid":"46f2a531-af05-423f-a504-cee642327336","status":"0","description":null,"created_time":"2025-12-04 21:46:20","updated_time":"2025-12-04 21:55:37","name":"自定义102","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2_1","password":"$2b$12$pINs3SFXdC3qqu6NiM8Yr.P54ITt1LUMrZ1tljdPpjhwhwK65oQ06","is_superuser":false,"dept_id":7,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:50:01","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":7,"name":"test2_1"},"positions":[],"roles":[{"id":6,"uuid":"96f6a404-d6b0-4a46-b6fa-5cbd56e42739","status":"0","description":null,"created_time":"2025-12-04 21:32:02","updated_time":"2025-12-04 21:32:35","name":"自定义数据","code":"ZIDINGYI","order":1,"data_scope":5,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null}],"depts":[{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.45s	60	43404166-5f24-4cf4-8887-504ec82d52b5	0	修改用户	2025-12-04 21:55:37.143858	2025-12-04 21:55:37.143861	1	1
2	/api/v1/system/user/update/4	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":4,"uuid":"0164b4be-69e8-437e-9b37-87727eae3964","status":"0","description":null,"created_time":"2025-12-04 21:41:51","updated_time":"2025-12-04 21:56:47","name":"全部数据","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1_1","password":"$2b$12$LtnJLJi9JP7QcIag70cIxOmkvdIFyZQFNOTbfTZtkBXITSYjmkF7C","is_superuser":false,"dept_id":4,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:48:26","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":4,"name":"test1_1"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.52s	61	75959b65-05aa-4a44-a436-05ca7d4646a9	0	修改用户	2025-12-04 21:56:47.579065	2025-12-04 21:56:47.579069	1	1
2	/api/v1/system/user/update/4	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":4,"uuid":"0164b4be-69e8-437e-9b37-87727eae3964","status":"0","description":null,"created_time":"2025-12-04 21:41:51","updated_time":"2025-12-04 21:58:06","name":"全部数据","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1_1","password":"$2b$12$vi1piWtcFTJ8IpcbFgGnIOdd/Ab9hGTHxD2jtVDHVQpiFd758BagG","is_superuser":false,"dept_id":4,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:48:26","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":4,"name":"test1_1"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.64s	64	cde08641-c508-484c-91b7-3d6ffecb5067	0	修改用户	2025-12-04 21:58:06.450395	2025-12-04 21:58:06.4504	1	1
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjY4YjZiY2JjLTU5ODItNGI4ZC1iMTlhLWIzMDEwOTg4ODFkM1wiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTE6MTFcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTA3MX0.SjvHPXMlw2GowjGWP8HN7hQiIgWCLR7Oy0Kpchk_zys"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.03s	62	fa51d7bb-ddba-4f12-8cc8-e518112ec325	0	退出登录	2025-12-04 21:57:00.324043	2025-12-04 21:57:00.324046	1	1
1	/api/v1/system/auth/login	POST	username: admin\npassword: 123456\ncaptcha: 5\ncaptcha_key: 434a3102aeee4253a36cc5b1f03666b0\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjYwMTk3NGIwLTUwM2MtNGM1ZS05NmY5LTU5YzRkMTA2YzQ3M1wiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTc6MzFcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTQ1MX0.2-Ptz87wxGbBLi8E-b3kiGOv0vJZ9LX9LP4Do9LY-aA","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjYwMTk3NGIwLTUwM2MtNGM1ZS05NmY5LTU5YzRkMTA2YzQ3M1wiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTc6MzFcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTczNDUxfQ.DxhLmq7vS0dsLy4itsPRg1XrnX0THWeZpSM-DDJMWNc","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.32s	63	8692b024-1619-49c1-9ce6-a6658dae84bc	0	登录	2025-12-04 21:57:31.138762	2025-12-04 21:57:31.138764	\N	\N
2	/api/v1/system/user/reset/password	PUT	{"body": {"id": 4, "password": "123456"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"重置密码成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":4,"uuid":"0164b4be-69e8-437e-9b37-87727eae3964","status":"0","description":null,"created_time":"2025-12-04 21:41:51","updated_time":"2025-12-04 22:02:06","name":"全部数据","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1_1","password":"$2b$12$M/KNhjFGMdr0nm0HmZm7JeEc3eb8PZKkX1WCgsqZq.z0Gju6J7UG6","is_superuser":false,"dept_id":4,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:48:26","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":4,"name":"test1_1"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.49s	65	5fe11ef0-074d-4e1d-acc0-d7eb4b7e7ab1	0	重置密码	2025-12-04 22:02:06.769181	2025-12-04 22:02:06.769186	1	1
2	/api/v1/system/user/reset/password	PUT	{"body": {"id": 6, "password": "123456"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"重置密码成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":6,"uuid":"46f2a531-af05-423f-a504-cee642327336","status":"0","description":null,"created_time":"2025-12-04 21:46:20","updated_time":"2025-12-04 22:02:10","name":"自定义102","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2_1","password":"$2b$12$QaSuhXtbd32TclDQX.sle.rW2ByUM36ld0t46psEEbYKRIFLiZxWu","is_superuser":false,"dept_id":7,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:50:01","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":7,"name":"test2_1"},"positions":[],"roles":[{"id":6,"uuid":"96f6a404-d6b0-4a46-b6fa-5cbd56e42739","status":"0","description":null,"created_time":"2025-12-04 21:32:02","updated_time":"2025-12-04 21:32:35","name":"自定义数据","code":"ZIDINGYI","order":1,"data_scope":5,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null}],"depts":[{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.40s	66	ccda49c8-8498-4a1f-9b8d-6413e5e4cef6	0	重置密码	2025-12-04 22:02:10.501869	2025-12-04 22:02:10.501871	1	1
2	/api/v1/system/user/reset/password	PUT	{"body": {"id": 5, "password": "123456"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"重置密码成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":5,"uuid":"b730fcb1-2cff-472c-9809-a4167313e6fb","status":"0","description":null,"created_time":"2025-12-04 21:44:44","updated_time":"2025-12-04 22:02:15","name":"仅个人","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1_2","password":"$2b$12$ZW6BK1WCEepwRgevC/.9n.TnSwsftYa9tYOiWpiuUEIcFE045Z5ma","is_superuser":false,"dept_id":5,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:49:24","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":5,"name":"test1_2"},"positions":[],"roles":[{"id":2,"uuid":"242f44f5-6faf-4245-aac7-482630ddb6f7","status":"0","description":null,"created_time":"2025-12-04 21:22:35","updated_time":"2025-12-04 21:29:46","name":"仅个人数据","code":"MINE","order":1,"data_scope":1,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.38s	67	9136b4aa-0ee4-4e30-af44-69ef73f305a0	0	重置密码	2025-12-04 22:02:15.737263	2025-12-04 22:02:15.73727	1	1
2	/api/v1/system/user/reset/password	PUT	{"body": {"id": 2, "password": "123456"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"重置密码成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":2,"uuid":"3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29","status":"0","description":null,"created_time":"2025-12-03 23:24:32","updated_time":"2025-12-04 22:02:19","name":"本部门及以下","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1","password":"$2b$12$GnAIyhOri8fJjgoCLRUTVOovW6bfIXLdRPh0YYE5RcV3bKdJgVz1S","is_superuser":false,"dept_id":2,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:47:00","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":2,"name":"test1"},"positions":[],"roles":[{"id":5,"uuid":"b419c2ef-af62-4d93-80e5-4afb24be9289","status":"0","description":null,"created_time":"2025-12-04 21:23:50","updated_time":"2025-12-04 21:30:14","name":"本部门及以下","code":"ALL_DEPT","order":1,"data_scope":3,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.38s	68	ff185f8b-ec97-4bb0-bf15-e25f7f6fb721	0	重置密码	2025-12-04 22:02:19.077285	2025-12-04 22:02:19.077288	1	1
2	/api/v1/system/user/reset/password	PUT	{"body": {"id": 3, "password": "123456"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"重置密码成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":3,"uuid":"4c2b0473-3130-4c4d-bebf-94412ea05c7e","status":"0","description":null,"created_time":"2025-12-04 21:41:18","updated_time":"2025-12-04 22:02:22","name":"本部门数据","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2","password":"$2b$12$VF1IjpXM1/Y604M4QE509OqtVHbTaEBkmPO0WfWxEqzm1gdveDBNi","is_superuser":false,"dept_id":3,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:47:37","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":3,"name":"test2"},"positions":[],"roles":[{"id":4,"uuid":"6a229f0d-7dcb-4b66-9054-987e3c1dfe5d","status":"0","description":null,"created_time":"2025-12-04 21:23:30","updated_time":"2025-12-04 21:29:59","name":"本部门数据","code":"DEPT","order":1,"data_scope":2,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.36s	69	0fe0fabc-54bc-4d8b-bfa4-cf967a3ab5a8	0	重置密码	2025-12-04 22:02:22.771204	2025-12-04 22:02:22.77121	1	1
2	/api/v1/system/user/reset/password	PUT	{"body": {"id": 7, "password": "123456"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"重置密码成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":7,"uuid":"da0c4cec-c428-4347-ba67-ec6b1878fc2c","status":"0","description":null,"created_time":"2025-12-04 21:46:42","updated_time":"2025-12-04 22:02:26","name":"test2_2","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2_2","password":"$2b$12$7VjR260GghaKx1BOczedTumXlsdab1iCSt4SiySCwUniAY8XcxAZu","is_superuser":false,"dept_id":6,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:50:36","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":6,"name":"test2_2"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.38s	70	f0dc22e8-cd51-4bb7-b44f-8ba213b682c6	0	重置密码	2025-12-04 22:02:26.549021	2025-12-04 22:02:26.549024	1	1
2	/api/v1/system/user/update/7	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":7,"uuid":"da0c4cec-c428-4347-ba67-ec6b1878fc2c","status":"0","description":null,"created_time":"2025-12-04 21:46:42","updated_time":"2025-12-04 22:02:26","name":"test2_2","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2_2","password":"$2b$12$7VjR260GghaKx1BOczedTumXlsdab1iCSt4SiySCwUniAY8XcxAZu","is_superuser":false,"dept_id":6,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:50:36","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":6,"name":"test2_2"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.25s	71	a6f94673-8e80-4064-b872-8d927b8945c2	0	修改用户	2025-12-04 22:02:38.245465	2025-12-04 22:02:38.245468	1	1
2	/api/v1/system/user/update/3	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":3,"uuid":"4c2b0473-3130-4c4d-bebf-94412ea05c7e","status":"0","description":null,"created_time":"2025-12-04 21:41:18","updated_time":"2025-12-04 22:02:22","name":"本部门数据","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2","password":"$2b$12$VF1IjpXM1/Y604M4QE509OqtVHbTaEBkmPO0WfWxEqzm1gdveDBNi","is_superuser":false,"dept_id":3,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:47:37","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":3,"name":"test2"},"positions":[],"roles":[{"id":4,"uuid":"6a229f0d-7dcb-4b66-9054-987e3c1dfe5d","status":"0","description":null,"created_time":"2025-12-04 21:23:30","updated_time":"2025-12-04 21:29:59","name":"本部门数据","code":"DEPT","order":1,"data_scope":2,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.19s	72	47b45aff-6bd7-4e40-8631-20fa650944d5	0	修改用户	2025-12-04 22:02:41.636772	2025-12-04 22:02:41.636776	1	1
2	/api/v1/system/user/update/2	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":2,"uuid":"3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29","status":"0","description":null,"created_time":"2025-12-03 23:24:32","updated_time":"2025-12-04 22:02:19","name":"本部门及以下","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1","password":"$2b$12$GnAIyhOri8fJjgoCLRUTVOovW6bfIXLdRPh0YYE5RcV3bKdJgVz1S","is_superuser":false,"dept_id":2,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:47:00","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":2,"name":"test1"},"positions":[],"roles":[{"id":5,"uuid":"b419c2ef-af62-4d93-80e5-4afb24be9289","status":"0","description":null,"created_time":"2025-12-04 21:23:50","updated_time":"2025-12-04 21:30:14","name":"本部门及以下","code":"ALL_DEPT","order":1,"data_scope":3,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.19s	73	b40f3fe8-0331-4bf6-a49e-bd11405e5801	0	修改用户	2025-12-04 22:02:44.93788	2025-12-04 22:02:44.937883	1	1
2	/api/v1/system/user/update/5	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":5,"uuid":"b730fcb1-2cff-472c-9809-a4167313e6fb","status":"0","description":null,"created_time":"2025-12-04 21:44:44","updated_time":"2025-12-04 22:02:15","name":"仅个人","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1_2","password":"$2b$12$ZW6BK1WCEepwRgevC/.9n.TnSwsftYa9tYOiWpiuUEIcFE045Z5ma","is_superuser":false,"dept_id":5,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:49:24","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":5,"name":"test1_2"},"positions":[],"roles":[{"id":2,"uuid":"242f44f5-6faf-4245-aac7-482630ddb6f7","status":"0","description":null,"created_time":"2025-12-04 21:22:35","updated_time":"2025-12-04 21:29:46","name":"仅个人数据","code":"MINE","order":1,"data_scope":1,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.20s	74	fa3fab6e-3fbc-409c-9088-8e04590de519	0	修改用户	2025-12-04 22:02:47.792483	2025-12-04 22:02:47.792486	1	1
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcImM4YjZjMjUwLWY2ODQtNGNhNi1iMDcyLTlkMGM5MDYwY2IyYlwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDU6MjBcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTkyMH0.9eMvBVxsZyPyKep6UGgnTwqOMds8clxJe4dqpXfMauA"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.02s	86	32ac18ee-6c90-44e6-9d7c-15ad8181509e	0	退出登录	2025-12-04 22:06:33.040341	2025-12-04 22:06:33.040343	1	1
2	/api/v1/system/user/update/6	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":6,"uuid":"46f2a531-af05-423f-a504-cee642327336","status":"0","description":null,"created_time":"2025-12-04 21:46:20","updated_time":"2025-12-04 22:02:10","name":"自定义102","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2_1","password":"$2b$12$QaSuhXtbd32TclDQX.sle.rW2ByUM36ld0t46psEEbYKRIFLiZxWu","is_superuser":false,"dept_id":7,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:50:01","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":7,"name":"test2_1"},"positions":[],"roles":[{"id":6,"uuid":"96f6a404-d6b0-4a46-b6fa-5cbd56e42739","status":"0","description":null,"created_time":"2025-12-04 21:32:02","updated_time":"2025-12-04 21:32:35","name":"自定义数据","code":"ZIDINGYI","order":1,"data_scope":5,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null}],"depts":[{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.19s	75	0e81ebdb-de0e-43df-b74b-c65c1e6c7494	0	修改用户	2025-12-04 22:02:50.810443	2025-12-04 22:02:50.810446	1	1
2	/api/v1/system/user/update/4	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":4,"uuid":"0164b4be-69e8-437e-9b37-87727eae3964","status":"0","description":null,"created_time":"2025-12-04 21:41:51","updated_time":"2025-12-04 22:02:06","name":"全部数据","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test1_1","password":"$2b$12$M/KNhjFGMdr0nm0HmZm7JeEc3eb8PZKkX1WCgsqZq.z0Gju6J7UG6","is_superuser":false,"dept_id":4,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:48:26","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":4,"name":"test1_1"},"positions":[],"roles":[{"id":3,"uuid":"91131798-462f-498a-a4c8-e2df5f8ebdb6","status":"0","description":null,"created_time":"2025-12-04 21:23:11","updated_time":"2025-12-04 21:30:37","name":"全部数据","code":"ALL","order":1,"data_scope":4,"menus":[{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null}],"depts":[{"id":1,"uuid":"8b0a0481-23fd-45b6-bb77-44090af2db2d","status":"0","description":"集团总公司","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"集团总公司","order":1,"code":"GROUP","leader":"部门负责人","phone":"1582112620","email":"deptadmin@example.com","parent_id":null,"parent_name":null},{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":3,"uuid":"e765168f-6ade-4c5d-9c3f-7ba94cce5ade","status":"0","description":null,"created_time":"2025-12-04 21:16:35","updated_time":"2025-12-04 21:16:35","name":"test2","order":1,"code":"test2","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null},{"id":4,"uuid":"0e9b15e1-acaa-4de6-974e-f59154ed7dde","status":"0","description":null,"created_time":"2025-12-04 21:16:46","updated_time":"2025-12-04 21:16:46","name":"test1_1","order":1,"code":"test1_1","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":5,"uuid":"07ef4871-5f55-49f0-87f0-1a9b28017c5c","status":"0","description":null,"created_time":"2025-12-04 21:17:23","updated_time":"2025-12-04 21:17:23","name":"test1_2","order":1,"code":"test1_2","leader":null,"phone":null,"email":null,"parent_id":2,"parent_name":null},{"id":6,"uuid":"8a640047-7c0f-42ef-84a1-0ec7d994d5ce","status":"0","description":null,"created_time":"2025-12-04 21:17:36","updated_time":"2025-12-04 21:17:36","name":"test2_2","order":1,"code":"test2_2","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null},{"id":7,"uuid":"fee2602e-77ff-406b-8151-9774f3d99a07","status":"0","description":null,"created_time":"2025-12-04 21:17:46","updated_time":"2025-12-04 21:17:46","name":"test2_1","order":1,"code":"test2_1","leader":null,"phone":null,"email":null,"parent_id":3,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.19s	76	9c728169-7558-446f-ae89-39b6cdcaf93e	0	修改用户	2025-12-04 22:02:53.607789	2025-12-04 22:02:53.607793	1	1
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjYwMTk3NGIwLTUwM2MtNGM1ZS05NmY5LTU5YzRkMTA2YzQ3M1wiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTM6NTc6MzFcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTQ1MX0.2-Ptz87wxGbBLi8E-b3kiGOv0vJZ9LX9LP4Do9LY-aA"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.03s	77	9e14e900-1b30-4c04-85a2-fd3c77ae2c33	0	退出登录	2025-12-04 22:03:10.233995	2025-12-04 22:03:10.233998	1	1
1	/api/v1/system/auth/login	POST	username: test1_2\npassword: 123456\ncaptcha: 16\ncaptcha_key: 8d069de2446441b38f1b2bee3fcf83e4\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTRlYzVcdTRlMmFcdTRlYmFcIixcInNlc3Npb25faWRcIjpcImUwM2JlNjRmLTUyOTUtNGY5MC04NjQ2LTk2M2ZiODgwMDY0NVwiLFwidXNlcl9pZFwiOjUsXCJ1c2VyX25hbWVcIjpcInRlc3QxXzJcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxNDowMzoyMVwiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjpmYWxzZSwiZXhwIjoxNzcwMDY5ODAxfQ.wE4kAD1waqi5gczR02xTV61O_pzm20dlcsgaIo8j3qg","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTRlYzVcdTRlMmFcdTRlYmFcIixcInNlc3Npb25faWRcIjpcImUwM2JlNjRmLTUyOTUtNGY5MC04NjQ2LTk2M2ZiODgwMDY0NVwiLFwidXNlcl9pZFwiOjUsXCJ1c2VyX25hbWVcIjpcInRlc3QxXzJcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxNDowMzoyMVwiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjp0cnVlLCJleHAiOjE4MDExNzM4MDF9.FxuWycWCX7Hj3itYp4vgszKmFcSA0pnkMo-gbFjoWmc","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.39s	78	a42241ac-6992-4795-ac68-781495b96c21	0	登录	2025-12-04 22:03:21.875713	2025-12-04 22:03:21.875719	\N	\N
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTRlYzVcdTRlMmFcdTRlYmFcIixcInNlc3Npb25faWRcIjpcImUwM2JlNjRmLTUyOTUtNGY5MC04NjQ2LTk2M2ZiODgwMDY0NVwiLFwidXNlcl9pZFwiOjUsXCJ1c2VyX25hbWVcIjpcInRlc3QxXzJcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxNDowMzoyMVwiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjpmYWxzZSwiZXhwIjoxNzcwMDY5ODAxfQ.wE4kAD1waqi5gczR02xTV61O_pzm20dlcsgaIo8j3qg"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.04s	79	57b315b5-b94b-46ee-bfd7-a6ab93c932e0	0	退出登录	2025-12-04 22:03:33.460658	2025-12-04 22:03:33.46066	5	5
1	/api/v1/system/auth/login	POST	username: admin\npassword: 123456\ncaptcha: 2\ncaptcha_key: 6c6867b50a454644920ee6610d5d5148\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjExOTU0NzQ4LWU0YmQtNGY0Zi1hNTQzLWU4M2U4NTM2YTZhOVwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDM6MzhcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTgxOH0.ElvUIf5kV5gBVPI3_aH_8u4WVhpS0T2eBsDiyNZN44M","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjExOTU0NzQ4LWU0YmQtNGY0Zi1hNTQzLWU4M2U4NTM2YTZhOVwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDM6MzhcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTczODE4fQ.OtCIjAZydPF4qdl4z09bf_ibz7EJBTj1WbcnGTyUIqc","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.31s	80	c687c39e-cde8-4366-a86d-051718016c82	0	登录	2025-12-04 22:03:38.094421	2025-12-04 22:03:38.094423	\N	\N
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjExOTU0NzQ4LWU0YmQtNGY0Zi1hNTQzLWU4M2U4NTM2YTZhOVwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDM6MzhcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTgxOH0.ElvUIf5kV5gBVPI3_aH_8u4WVhpS0T2eBsDiyNZN44M"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.02s	81	092e5601-b4af-4136-ace7-dbf1eb6ac8cd	0	退出登录	2025-12-04 22:03:58.742496	2025-12-04 22:03:58.742498	1	1
1	/api/v1/system/auth/login	POST	username: test2\npassword: 123456\ncaptcha: 15\ncaptcha_key: 64d58cb49c3c44c0937b6ac0cb6b932c\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTY1NzBcdTYzNmVcIixcInNlc3Npb25faWRcIjpcImYyZTUzOWI5LTc2M2ItNDIzMS1iYTRhLWExMThhOTEyZTM2N1wiLFwidXNlcl9pZFwiOjMsXCJ1c2VyX25hbWVcIjpcInRlc3QyXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDQ6MDRcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTg0NH0.c4rueCEkXIOlwstfcxxRaeDzQQ6EwH_1x128Wv0CMxM","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTY1NzBcdTYzNmVcIixcInNlc3Npb25faWRcIjpcImYyZTUzOWI5LTc2M2ItNDIzMS1iYTRhLWExMThhOTEyZTM2N1wiLFwidXNlcl9pZFwiOjMsXCJ1c2VyX25hbWVcIjpcInRlc3QyXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDQ6MDRcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTczODQ0fQ.wEeTX7zjbkGWvaNrSBK1nMCBxVcTaPBGzN5VwXjAGEw","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.37s	82	b684375b-f387-4f78-b595-786270e53849	0	登录	2025-12-04 22:04:04.660549	2025-12-04 22:04:04.660552	\N	\N
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTY1NzBcdTYzNmVcIixcInNlc3Npb25faWRcIjpcImYyZTUzOWI5LTc2M2ItNDIzMS1iYTRhLWExMThhOTEyZTM2N1wiLFwidXNlcl9pZFwiOjMsXCJ1c2VyX25hbWVcIjpcInRlc3QyXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDQ6MDRcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTg0NH0.c4rueCEkXIOlwstfcxxRaeDzQQ6EwH_1x128Wv0CMxM"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.06s	83	d300cdd0-9b15-486c-9401-97a5b82ca8c8	0	退出登录	2025-12-04 22:05:12.650778	2025-12-04 22:05:12.650782	3	3
1	/api/v1/system/auth/login	POST	username: admin\npassword: 123456\ncaptcha: 5\ncaptcha_key: cb7059b126c642709230b732263bcb13\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcImM4YjZjMjUwLWY2ODQtNGNhNi1iMDcyLTlkMGM5MDYwY2IyYlwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDU6MjBcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA2OTkyMH0.9eMvBVxsZyPyKep6UGgnTwqOMds8clxJe4dqpXfMauA","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcImM4YjZjMjUwLWY2ODQtNGNhNi1iMDcyLTlkMGM5MDYwY2IyYlwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDU6MjBcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTczOTIwfQ.LfdYrQNopsdfCMfb1uQycvv-CAe_NH_HkZ6MbMcFX2k","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.31s	84	3571c67d-48ee-4a8a-8889-b34f4dcb1656	0	登录	2025-12-04 22:05:20.535673	2025-12-04 22:05:20.535679	\N	\N
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjZiOTM3YWFjLTRjN2YtNGIzNC1hZDE3LWNmMTMyNTVkY2RmNlwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDc6MjNcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA3MDA0M30.JE5Ed32a6ERCy2Rsn-RNW48Lr24BuQ5Zhncg8YVBW00"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.03s	93	3584cc0a-692e-45f9-975a-259276560d50	0	退出登录	2025-12-04 22:08:06.987687	2025-12-04 22:08:06.987694	1	1
1	/api/v1/system/auth/login	POST	username: test1\npassword: 123456\ncaptcha: 6\ncaptcha_key: 9a6882b23e804bf0affdce9011a03c8e\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTUzY2FcdTRlZTVcdTRlMGJcIixcInNlc3Npb25faWRcIjpcImUwN2I3Y2JkLThhOGMtNDJiZC04ZDcxLWY1M2M4YmMwZjAwMFwiLFwidXNlcl9pZFwiOjIsXCJ1c2VyX25hbWVcIjpcInRlc3QxXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDg6MTVcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA3MDA5NX0.vjWnIUN0vpO95EjKOXQG8gmYc2JFUmCu4mzjAlDhgno","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTUzY2FcdTRlZTVcdTRlMGJcIixcInNlc3Npb25faWRcIjpcImUwN2I3Y2JkLThhOGMtNDJiZC04ZDcxLWY1M2M4YmMwZjAwMFwiLFwidXNlcl9pZFwiOjIsXCJ1c2VyX25hbWVcIjpcInRlc3QxXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDg6MTVcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTc0MDk1fQ.sZ17BVKJUjA_5JhB8j0q165ZImK2W2RTRQqm1pkLcWU","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.39s	94	6569502e-d9cc-49e8-9010-f888573234d9	0	登录	2025-12-04 22:08:15.373939	2025-12-04 22:08:15.373941	\N	\N
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTUzY2FcdTRlZTVcdTRlMGJcIixcInNlc3Npb25faWRcIjpcImUwN2I3Y2JkLThhOGMtNDJiZC04ZDcxLWY1M2M4YmMwZjAwMFwiLFwidXNlcl9pZFwiOjIsXCJ1c2VyX25hbWVcIjpcInRlc3QxXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDg6MTVcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA3MDA5NX0.vjWnIUN0vpO95EjKOXQG8gmYc2JFUmCu4mzjAlDhgno"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.07s	95	16259d76-f23d-4d80-901b-7c751644193e	0	退出登录	2025-12-04 22:08:27.419686	2025-12-04 22:08:27.419689	2	2
1	/api/v1/system/auth/login	POST	username: test22\npassword: 123456\ncaptcha: 3\ncaptcha_key: 181a8232308649a8a7bf469cda0b68a2\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTY1NzBcdTYzNmUyXCIsXCJzZXNzaW9uX2lkXCI6XCIwZTkyMWVjNi0zNzA3LTRmOTgtODA2MC0yNzdmNmFhMjY2MGRcIixcInVzZXJfaWRcIjo4LFwidXNlcl9uYW1lXCI6XCJ0ZXN0MjJcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxNDowNjozN1wiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjpmYWxzZSwiZXhwIjoxNzcwMDY5OTk3fQ.uNWYal0j-tzgZvG1utd23EeMldbJ93yYGidRMnNiAhc","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTY1NzBcdTYzNmUyXCIsXCJzZXNzaW9uX2lkXCI6XCIwZTkyMWVjNi0zNzA3LTRmOTgtODA2MC0yNzdmNmFhMjY2MGRcIixcInVzZXJfaWRcIjo4LFwidXNlcl9uYW1lXCI6XCJ0ZXN0MjJcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxNDowNjozN1wiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjp0cnVlLCJleHAiOjE4MDExNzM5OTd9.6fNBjeOy_XOTgwCCR73aiLQxkJkBpOLqDzFz6jHlTug","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.42s	87	9d46d498-613f-4011-b430-1066f84e397f	0	登录	2025-12-04 22:06:37.735517	2025-12-04 22:06:37.735519	\N	\N
2	/api/v1/gencode/demo/create	POST	{"body": {"name": "test22", "status": "0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"创建示例成功","data":{"created_id":8,"created_by":{"id":8,"name":"本部门数据2","username":"test22"},"updated_id":8,"updated_by":{"id":8,"name":"本部门数据2","username":"test22"},"id":9,"uuid":"f20abab2-39bb-4797-8d42-d46707b80c26","status":"0","description":null,"created_time":"2025-12-04 22:06:49","updated_time":"2025-12-04 22:06:49","name":"test22"},"status_code":200,"success":true}	0.06s	88	f829b7fd-0a85-4f53-9e8a-ebce4d2358f3	0	创建示例	2025-12-04 22:06:49.462366	2025-12-04 22:06:49.462369	8	8
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTY1NzBcdTYzNmUyXCIsXCJzZXNzaW9uX2lkXCI6XCIwZTkyMWVjNi0zNzA3LTRmOTgtODA2MC0yNzdmNmFhMjY2MGRcIixcInVzZXJfaWRcIjo4LFwidXNlcl9uYW1lXCI6XCJ0ZXN0MjJcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxNDowNjozN1wiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjpmYWxzZSwiZXhwIjoxNzcwMDY5OTk3fQ.uNWYal0j-tzgZvG1utd23EeMldbJ93yYGidRMnNiAhc"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.04s	89	b0620f41-1461-49a5-9f76-fb574e4274c7	0	退出登录	2025-12-04 22:07:02.269242	2025-12-04 22:07:02.269244	8	8
1	/api/v1/system/auth/login	POST	username: test2\npassword: 123456\ncaptcha: 4\ncaptcha_key: 149511ab75e440a6aefb0e9c28195f5a\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTY1NzBcdTYzNmVcIixcInNlc3Npb25faWRcIjpcImRjNTdlZDAyLTZlNWUtNDNmMi1hMWU5LWNjYWEyM2QxYTZiY1wiLFwidXNlcl9pZFwiOjMsXCJ1c2VyX25hbWVcIjpcInRlc3QyXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDc6MTBcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA3MDAzMH0.APwqFnfR-js6TSqSwIYOqX2fjIYj0pX-hq1_eCMcKfs","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTY1NzBcdTYzNmVcIixcInNlc3Npb25faWRcIjpcImRjNTdlZDAyLTZlNWUtNDNmMi1hMWU5LWNjYWEyM2QxYTZiY1wiLFwidXNlcl9pZFwiOjMsXCJ1c2VyX25hbWVcIjpcInRlc3QyXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDc6MTBcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTc0MDMwfQ.nd7K6kSW0kJBy-xk2a5Nr3aP_vuKikCAsajyjSSPrKs","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.37s	90	e040d153-f77e-4173-b697-17558836e6a5	0	登录	2025-12-04 22:07:10.926981	2025-12-04 22:07:10.926987	\N	\N
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTY3MmNcdTkwZThcdTk1ZThcdTY1NzBcdTYzNmVcIixcInNlc3Npb25faWRcIjpcImRjNTdlZDAyLTZlNWUtNDNmMi1hMWU5LWNjYWEyM2QxYTZiY1wiLFwidXNlcl9pZFwiOjMsXCJ1c2VyX25hbWVcIjpcInRlc3QyXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDc6MTBcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA3MDAzMH0.APwqFnfR-js6TSqSwIYOqX2fjIYj0pX-hq1_eCMcKfs"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.06s	91	601ca8ed-8529-4fd8-9eaa-c50925066181	0	退出登录	2025-12-04 22:07:18.866271	2025-12-04 22:07:18.866274	3	3
1	/api/v1/system/auth/login	POST	username: admin\npassword: 123456\ncaptcha: 3\ncaptcha_key: 8a2da5da65d840459d0c178e2cfcbcce\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjZiOTM3YWFjLTRjN2YtNGIzNC1hZDE3LWNmMTMyNTVkY2RmNlwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDc6MjNcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA3MDA0M30.JE5Ed32a6ERCy2Rsn-RNW48Lr24BuQ5Zhncg8YVBW00","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcIjZiOTM3YWFjLTRjN2YtNGIzNC1hZDE3LWNmMTMyNTVkY2RmNlwiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDc6MjNcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTc0MDQzfQ.5CfK5pRIi6eIoK5rIvyrW47XgZo4S4h51mMmQaiKCZc","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.30s	92	df2aab64-2271-42fb-975f-b4e460a182b5	0	登录	2025-12-04 22:07:23.098292	2025-12-04 22:07:23.098294	\N	\N
1	/api/v1/system/auth/login	POST	username: test1_1\npassword: 123456\ncaptcha: 7\ncaptcha_key: 2335327deb8b499983b2d2480fae4c15\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTUxNjhcdTkwZThcdTY1NzBcdTYzNmVcIixcInNlc3Npb25faWRcIjpcIjY1MWEyZGMwLTFjNWMtNDU5OC1hZmUxLTRhMGQ0NDgxYzFjYVwiLFwidXNlcl9pZFwiOjQsXCJ1c2VyX25hbWVcIjpcInRlc3QxXzFcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxNDowODozOFwiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjpmYWxzZSwiZXhwIjoxNzcwMDcwMTE4fQ.aBYXU5VtOzHQ9ROpMZAke_HFBxexY07yM59WQ7yEt7A","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTUxNjhcdTkwZThcdTY1NzBcdTYzNmVcIixcInNlc3Npb25faWRcIjpcIjY1MWEyZGMwLTFjNWMtNDU5OC1hZmUxLTRhMGQ0NDgxYzFjYVwiLFwidXNlcl9pZFwiOjQsXCJ1c2VyX25hbWVcIjpcInRlc3QxXzFcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxNDowODozOFwiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjp0cnVlLCJleHAiOjE4MDExNzQxMTh9.ScsjeZPEqK7Lfq9XXpRVjl8IKA7Y01oPKF49_jsCs2Q","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.36s	96	89e174f7-9d3f-432a-88f7-b4bb8eb4842a	0	登录	2025-12-04 22:08:38.604704	2025-12-04 22:08:38.604706	\N	\N
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTUxNjhcdTkwZThcdTY1NzBcdTYzNmVcIixcInNlc3Npb25faWRcIjpcIjY1MWEyZGMwLTFjNWMtNDU5OC1hZmUxLTRhMGQ0NDgxYzFjYVwiLFwidXNlcl9pZFwiOjQsXCJ1c2VyX25hbWVcIjpcInRlc3QxXzFcIixcImlwYWRkclwiOlwiMTI3LjAuMC4xXCIsXCJsb2dpbl9sb2NhdGlvblwiOlwiXHU1MTg1XHU3ZjUxSVBcIixcIm9zXCI6XCJNYWMgT1MgWFwiLFwiYnJvd3NlclwiOlwiRWRnZVwiLFwibG9naW5fdGltZVwiOlwiMjAyNS0xMi0wNCAxNDowODozOFwiLFwibG9naW5fdHlwZVwiOlwiUENcdTdhZWZcIn0iLCJpc19yZWZyZXNoIjpmYWxzZSwiZXhwIjoxNzcwMDcwMTE4fQ.aBYXU5VtOzHQ9ROpMZAke_HFBxexY07yM59WQ7yEt7A"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.05s	97	11a3111c-eeeb-4c1c-a98c-e379e62860e0	0	退出登录	2025-12-04 22:08:59.947727	2025-12-04 22:08:59.94773	4	4
1	/api/v1/system/auth/login	POST	username: admin\npassword: 123456\ncaptcha: 16\ncaptcha_key: 0fb09d52d04e424c98df878499108983\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcImI1ZTMzMmFmLWRhMTctNGU4NS1iMGE5LTNkYzI5YzViNjIxY1wiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDk6MDhcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA3MDE0OH0.oEjEQrmg5UwlvRBJwSvmsPI8HZR3voEYkPeUj_eE9q0","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcImI1ZTMzMmFmLWRhMTctNGU4NS1iMGE5LTNkYzI5YzViNjIxY1wiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDk6MDhcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTc0MTQ4fQ.zkjo3YJpjomvxwl91UQfk4zTIdCmrg0UELxODfMekuY","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.35s	98	e926846f-16d1-41f0-82d7-9fbe246a4fff	0	登录	2025-12-04 22:09:08.054737	2025-12-04 22:09:08.05474	\N	\N
2	/api/v1/system/role/permission/setting	PATCH	{"body": {"role_ids": [6], "menu_ids": [7, 29, 106, 107, 108, 109, 110, 111, 112], "data_scope": 5, "dept_ids": [2]}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"授权角色成功","data":null,"status_code":200,"success":true}	0.11s	99	2d5a8486-7b50-4893-a3af-583397e94c70	0	角色授权	2025-12-04 22:10:03.401169	2025-12-04 22:10:03.401172	1	1
2	/api/v1/system/user/update/6	PUT	请求参数过长	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"修改用户成功","data":{"created_id":1,"created_by":{"id":1,"name":"超级管理员","username":"admin"},"updated_id":1,"updated_by":{"id":1,"name":"超级管理员","username":"admin"},"id":6,"uuid":"46f2a531-af05-423f-a504-cee642327336","status":"0","description":null,"created_time":"2025-12-04 21:46:20","updated_time":"2025-12-04 22:10:33","name":"自定义1","mobile":null,"email":null,"gender":"2","avatar":null,"username":"test2_1","password":"$2b$12$QaSuhXtbd32TclDQX.sle.rW2ByUM36ld0t46psEEbYKRIFLiZxWu","is_superuser":false,"dept_id":7,"role_ids":[],"position_ids":[],"last_login":"2025-12-04 13:50:01","gitee_login":null,"github_login":null,"wx_login":null,"qq_login":null,"dept_name":null,"dept":{"id":7,"name":"test2_1"},"positions":[],"roles":[{"id":6,"uuid":"96f6a404-d6b0-4a46-b6fa-5cbd56e42739","status":"0","description":null,"created_time":"2025-12-04 21:32:02","updated_time":"2025-12-04 22:10:03","name":"自定义数据","code":"ZIDINGYI","order":1,"data_scope":5,"menus":[{"id":106,"uuid":"0765e72d-cc91-49b9-bdc5-147868f00f1e","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"创建示例","type":3,"order":1,"permission":"module_gencode:demo:create","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"创建示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":29,"uuid":"73f4654d-16aa-404d-8319-043f4e237c70","status":"0","description":"示例管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"示例管理","type":2,"order":1,"permission":"module_gencode:demo:query","icon":"menu","route_name":"Demo","route_path":"/gencode/demo","component_path":"module_gencode/demo/index","redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"示例管理","params":null,"affix":false,"parent_id":7,"parent_name":null},{"id":107,"uuid":"0d9973c9-bf73-4f8a-a0c8-0b7477e955c5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"更新示例","type":3,"order":2,"permission":"module_gencode:demo:update","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"更新示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":108,"uuid":"c10732c4-7d4d-4a18-b55a-e879915e7821","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"删除示例","type":3,"order":3,"permission":"module_gencode:demo:delete","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"删除示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":109,"uuid":"46a710af-cc8a-4c84-8628-cfecde988dd9","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"批量修改示例状态","type":3,"order":4,"permission":"module_gencode:demo:patch","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"批量修改示例状态","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":110,"uuid":"64ca18eb-01c8-492c-a828-2beae7805de5","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导出示例","type":3,"order":5,"permission":"module_gencode:demo:export","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导出示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":111,"uuid":"b83aa5af-9acc-43a8-874f-b5042ac10875","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"导入示例","type":3,"order":6,"permission":"module_gencode:demo:import","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"导入示例","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":112,"uuid":"9a32c6b9-705b-45f5-92d8-583d7dca1b96","status":"0","description":"初始化数据","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"下载导入示例模版","type":3,"order":7,"permission":"module_gencode:demo:download","icon":null,"route_name":null,"route_path":null,"component_path":null,"redirect":null,"hidden":false,"keep_alive":true,"always_show":false,"title":"下载导入示例模版","params":null,"affix":false,"parent_id":29,"parent_name":null},{"id":7,"uuid":"3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a","status":"0","description":"模块管理","created_time":"2025-12-03 23:23:58","updated_time":"2025-12-03 23:23:58","name":"模块管理","type":1,"order":7,"permission":null,"icon":"menu","route_name":"Gencode","route_path":"/gencode","component_path":null,"redirect":"/gencode/demo","hidden":false,"keep_alive":false,"always_show":false,"title":"模块管理","params":null,"affix":false,"parent_id":null,"parent_name":null}],"depts":[{"id":2,"uuid":"aa1ee42b-7369-49f6-badb-a3784f57bbfa","status":"0","description":null,"created_time":"2025-12-04 21:16:25","updated_time":"2025-12-04 21:16:25","name":"test1","order":1,"code":"test1","leader":null,"phone":null,"email":null,"parent_id":1,"parent_name":null}]}],"menus":[]},"status_code":200,"success":true}	0.22s	100	6dced810-ec9c-4314-986f-00c961ce2c40	0	修改用户	2025-12-04 22:10:33.430339	2025-12-04 22:10:33.430343	1	1
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdThkODVcdTdlYTdcdTdiYTFcdTc0MDZcdTU0NThcIixcInNlc3Npb25faWRcIjpcImI1ZTMzMmFmLWRhMTctNGU4NS1iMGE5LTNkYzI5YzViNjIxY1wiLFwidXNlcl9pZFwiOjEsXCJ1c2VyX25hbWVcIjpcImFkbWluXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MDk6MDhcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA3MDE0OH0.oEjEQrmg5UwlvRBJwSvmsPI8HZR3voEYkPeUj_eE9q0"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.02s	101	c55730de-0dc7-434b-a9f3-0db0e01f1c09	0	退出登录	2025-12-04 22:10:40.037882	2025-12-04 22:10:40.037884	1	1
1	/api/v1/system/auth/login	POST	username: test2_1\npassword: 123456\ncaptcha: 11\ncaptcha_key: 12c159ac8a1a4efd9b0486cb2516a659\nremember: true\nlogin_type: PC端	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"登录成功","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTgxZWFcdTViOWFcdTRlNDkxXCIsXCJzZXNzaW9uX2lkXCI6XCI3YjgzNDUzNi01OGYzLTQ2MzktYjA4My1jY2M2YTI1YjQzMGJcIixcInVzZXJfaWRcIjo2LFwidXNlcl9uYW1lXCI6XCJ0ZXN0Ml8xXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MTA6NDVcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA3MDI0NX0.gBhS7Q2YYhOxlSS8sZBlrKu8gUaMn8OaWyUvRyQckCY","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTgxZWFcdTViOWFcdTRlNDkxXCIsXCJzZXNzaW9uX2lkXCI6XCI3YjgzNDUzNi01OGYzLTQ2MzktYjA4My1jY2M2YTI1YjQzMGJcIixcInVzZXJfaWRcIjo2LFwidXNlcl9uYW1lXCI6XCJ0ZXN0Ml8xXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MTA6NDVcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6dHJ1ZSwiZXhwIjoxODAxMTc0MjQ1fQ.97R7iXDZmWOZaTmuW1N8v6L-hrQ-AjLOhwmGk7THGkY","token_type":"bearer","expires_in":5184000},"status_code":200,"success":true}	0.36s	102	08f22b12-7392-4c66-be49-ebf783d6f3d6	0	登录	2025-12-04 22:10:45.631242	2025-12-04 22:10:45.631244	\N	\N
2	/api/v1/system/auth/logout	POST	{"body": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ7XCJuYW1lXCI6XCJcdTgxZWFcdTViOWFcdTRlNDkxXCIsXCJzZXNzaW9uX2lkXCI6XCI3YjgzNDUzNi01OGYzLTQ2MzktYjA4My1jY2M2YTI1YjQzMGJcIixcInVzZXJfaWRcIjo2LFwidXNlcl9uYW1lXCI6XCJ0ZXN0Ml8xXCIsXCJpcGFkZHJcIjpcIjEyNy4wLjAuMVwiLFwibG9naW5fbG9jYXRpb25cIjpcIlx1NTE4NVx1N2Y1MUlQXCIsXCJvc1wiOlwiTWFjIE9TIFhcIixcImJyb3dzZXJcIjpcIkVkZ2VcIixcImxvZ2luX3RpbWVcIjpcIjIwMjUtMTItMDQgMTQ6MTA6NDVcIixcImxvZ2luX3R5cGVcIjpcIlBDXHU3YWVmXCJ9IiwiaXNfcmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc3MDA3MDI0NX0.gBhS7Q2YYhOxlSS8sZBlrKu8gUaMn8OaWyUvRyQckCY"}}	127.0.0.1	内网IP	Mac OS X	Edge	200	{"code":0,"msg":"退出成功","data":null,"status_code":200,"success":true}	0.04s	103	e1f4d6e1-825d-42e6-b67e-582bdd7af989	0	退出登录	2025-12-04 22:11:07.222027	2025-12-04 22:11:07.22203	6	6
\.


--
-- Data for Name: sys_menu; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_menu (name, type, "order", permission, icon, route_name, route_path, component_path, redirect, hidden, keep_alive, always_show, title, params, affix, parent_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
仪表盘	1	1		client	Dashboard	/dashboard	\N	/dashboard/workplace	f	t	t	仪表盘	null	f	\N	1	3dd77516-9e2b-4f34-86e1-a6dc775d8b40	0	初始化数据	2025-12-03 23:23:58.803639	2025-12-03 23:23:58.803643
系统管理	1	2	\N	system	System	/system	\N	/system/menu	f	t	f	系统管理	null	f	\N	2	4a6b04ae-4311-4b2e-8970-ea37c62d3751	0	初始化数据	2025-12-03 23:23:58.803647	2025-12-03 23:23:58.803648
应用管理	1	3	\N	el-icon-ShoppingBag	Application	/application	\N	/application/myapp	f	f	f	应用管理	null	f	\N	3	8e21fcc8-2bbf-447c-9c6d-a2c5eafdbd5e	0	初始化数据	2025-12-03 23:23:58.803651	2025-12-03 23:23:58.803651
监控管理	1	4	\N	monitor	Monitor	/monitor	\N	/monitor/online	f	f	f	监控管理	null	f	\N	4	7f4871de-352a-4950-9325-6af49f46c4c3	0	初始化数据	2025-12-03 23:23:58.803654	2025-12-03 23:23:58.803654
代码管理	1	5	\N	code	Generator	/generator	\N	/generator/gencode	f	f	f	代码管理	null	f	\N	5	a75dc354-cbc9-4bed-97be-03ef91b6626b	0	代码管理	2025-12-03 23:23:58.803657	2025-12-03 23:23:58.803657
接口管理	1	6	\N	document	Common	/common	\N	/common/docs	f	f	f	接口管理	null	f	\N	6	9f00a26f-97ee-43f2-889f-edf3f78e3954	0	初始化数据	2025-12-03 23:23:58.80366	2025-12-03 23:23:58.803661
模块管理	1	7	\N	menu	Gencode	/gencode	\N	/gencode/demo	f	f	f	模块管理	null	f	\N	7	3a3e0c3f-7ffd-438b-b165-f0fa889f6a0a	0	模块管理	2025-12-03 23:23:58.803664	2025-12-03 23:23:58.803664
工作台	2	1	dashboard:workplace:query	el-icon-PieChart	Workplace	/dashboard/workplace	dashboard/workplace	\N	f	t	f	工作台	null	f	1	8	7b907334-cb97-4ccb-a82d-8d8f62a4f0ce	0	初始化数据	2025-12-03 23:23:58.80771	2025-12-03 23:23:58.807712
菜单管理	2	1	module_system:menu:query	menu	Menu	/system/menu	module_system/menu/index	\N	f	t	f	菜单管理	null	f	2	9	03d248ae-2c66-4d5a-b378-b8c69297f908	0	初始化数据	2025-12-03 23:23:58.807716	2025-12-03 23:23:58.807717
部门管理	2	2	module_system:dept:query	tree	Dept	/system/dept	module_system/dept/index	\N	f	t	f	部门管理	null	f	2	10	d5adb4e4-bb9f-4573-bcef-c41da3f9483f	0	初始化数据	2025-12-03 23:23:58.80772	2025-12-03 23:23:58.80772
岗位管理	2	3	module_system:position:query	el-icon-Coordinate	Position	/system/position	module_system/position/index	\N	f	t	f	岗位管理	null	f	2	11	63ecfb57-8fa1-4195-8154-2e46a8292bfa	0	初始化数据	2025-12-03 23:23:58.807723	2025-12-03 23:23:58.807723
角色管理	2	4	module_system:role:query	role	Role	/system/role	module_system/role/index	\N	f	t	f	角色管理	null	f	2	12	8c353e4d-db05-4b09-ae93-f0a7cca6b8ea	0	初始化数据	2025-12-03 23:23:58.807726	2025-12-03 23:23:58.807726
用户管理	2	5	module_system:user:query	el-icon-User	User	/system/user	module_system/user/index	\N	f	t	f	用户管理	null	f	2	13	5140f36e-60d0-49f1-89b5-4c7abfc7bda1	0	初始化数据	2025-12-03 23:23:58.807728	2025-12-03 23:23:58.807729
日志管理	2	6	module_system:log:query	el-icon-Aim	Log	/system/log	module_system/log/index	\N	f	t	f	日志管理	null	f	2	14	e6d102d7-a63e-4ff6-a4f4-cbb9b04053b9	0	初始化数据	2025-12-03 23:23:58.807731	2025-12-03 23:23:58.807732
公告管理	2	7	module_system:notice:query	bell	Notice	/system/notice	module_system/notice/index	\N	f	t	f	公告管理	null	f	2	15	e635b6d3-fed3-4da9-941a-5989eadb80ae	0	初始化数据	2025-12-03 23:23:58.807734	2025-12-03 23:23:58.807735
参数管理	2	8	module_system:param:query	setting	Params	/system/param	module_system/param/index	\N	f	t	f	参数管理	null	f	2	16	841ba259-e06d-4ad2-94fd-54ded653f96b	0	初始化数据	2025-12-03 23:23:58.807737	2025-12-03 23:23:58.807737
字典管理	2	9	module_system:dict_type:query	dict	Dict	/system/dict	module_system/dict/index	\N	f	t	f	字典管理	null	f	2	17	2e4a843f-cfd8-48cd-8465-de94d3735a54	0	初始化数据	2025-12-03 23:23:58.80774	2025-12-03 23:23:58.80774
我的应用	2	1	module_application:myapp:query	el-icon-ShoppingCartFull	MYAPP	/application/myapp	module_application/myapp/index	\N	f	t	f	我的应用	null	f	3	18	bc43d664-cd07-4c13-a634-2106590ed455	0	初始化数据	2025-12-03 23:23:58.807743	2025-12-03 23:23:58.807743
任务管理	2	2	module_application:job:query	el-icon-DataLine	Job	/application/job	module_application/job/index	\N	f	t	f	任务管理	null	f	3	19	b46d0101-88d5-49d2-9839-e4e5019de495	0	初始化数据	2025-12-03 23:23:58.807746	2025-12-03 23:23:58.807746
AI智能助手	2	3	module_application:ai:chat	el-icon-ToiletPaper	AI	/application/ai	module_application/ai/index	\N	f	t	f	AI智能助手	null	f	3	20	4f45a110-89a4-421d-b977-aa0eefb26094	0	AI智能助手	2025-12-03 23:23:58.807748	2025-12-03 23:23:58.807749
流程管理	2	4	module_application:workflow:query	el-icon-ShoppingBag	Workflow	/application/workflow	module_application/workflow/index	\N	f	t	f	我的流程	null	f	3	21	d35b6cde-9472-4689-a9f8-69b34154f080	0	我的流程	2025-12-03 23:23:58.807751	2025-12-03 23:23:58.807752
在线用户	2	1	module_monitor:online:query	el-icon-Headset	MonitorOnline	/monitor/online	module_monitor/online/index	\N	f	f	f	在线用户	null	f	4	22	de046a76-d0ed-43b7-bf56-e88535a25e00	0	初始化数据	2025-12-03 23:23:58.807754	2025-12-03 23:23:58.807755
服务器监控	2	2	module_monitor:server:query	el-icon-Odometer	MonitorServer	/monitor/server	module_monitor/server/index	\N	f	f	f	服务器监控	null	f	4	23	f1c5eb19-6cd1-4cac-9c91-7dd3ba63794b	0	初始化数据	2025-12-03 23:23:58.807757	2025-12-03 23:23:58.807758
缓存监控	2	3	module_monitor:cache:query	el-icon-Stopwatch	MonitorCache	/monitor/cache	module_monitor/cache/index	\N	f	f	f	缓存监控	null	f	4	24	361cdc57-e239-4dec-9e04-5ea48ccfe93d	0	初始化数据	2025-12-03 23:23:58.80776	2025-12-03 23:23:58.807761
文件管理	2	4	module_monitor:resource:query	el-icon-Files	Resource	/monitor/resource	module_monitor/resource/index	\N	f	t	f	文件管理	null	f	4	25	04e1a5a1-56cd-4b03-8ba6-05fa04612b71	0	初始化数据	2025-12-03 23:23:58.807763	2025-12-03 23:23:58.807764
代码生成	2	1	module_generator:gencode:query	code	GenCode	/generator/gencode	module_generator/gencode/index	\N	f	t	f	代码生成	null	f	5	26	0ee66e61-2909-49d8-bbc9-d16ed4c20dbe	0	代码生成	2025-12-03 23:23:58.807766	2025-12-03 23:23:58.807766
Swagger文档	4	1	module_common:docs:query	api	Docs	/common/docs	module_common/docs/index	\N	f	f	f	Swagger文档	null	f	6	27	277e7c9e-a6f0-4888-ae5d-5d2c7102be44	0	初始化数据	2025-12-03 23:23:58.807769	2025-12-03 23:23:58.807769
Redoc文档	4	2	module_common:redoc:query	el-icon-Document	Redoc	/common/redoc	module_common/redoc/index	\N	f	f	f	Redoc文档	null	f	6	28	e686eb9e-7c01-4aac-bb48-47231acfb226	0	初始化数据	2025-12-03 23:23:58.807772	2025-12-03 23:23:58.807772
示例管理	2	1	module_gencode:demo:query	menu	Demo	/gencode/demo	module_gencode/demo/index	\N	f	t	f	示例管理	null	f	7	29	73f4654d-16aa-404d-8319-043f4e237c70	0	示例管理	2025-12-03 23:23:58.807775	2025-12-03 23:23:58.807775
创建菜单	3	1	module_system:menu:create	\N	\N	\N	\N	\N	f	t	f	创建菜单	null	f	9	30	67b6a22d-adb9-4c4b-8977-d25d74b8ffcb	0	初始化数据	2025-12-03 23:23:58.810893	2025-12-03 23:23:58.810894
修改菜单	3	2	module_system:menu:update	\N	\N	\N	\N	\N	f	t	f	修改菜单	null	f	9	31	36125a38-0e1e-434d-b272-43c886d3e00c	0	初始化数据	2025-12-03 23:23:58.810897	2025-12-03 23:23:58.810898
删除菜单	3	3	module_system:menu:delete	\N	\N	\N	\N	\N	f	t	f	删除菜单	null	f	9	32	70187dbe-d98b-4cdd-af3f-9fb493393418	0	初始化数据	2025-12-03 23:23:58.810901	2025-12-03 23:23:58.810901
批量修改菜单状态	3	4	module_system:menu:patch	\N	\N	\N	\N	\N	f	t	f	批量修改菜单状态	null	f	9	33	0c66e39f-9f00-4b5f-af22-4abbf9e7c5d7	0	初始化数据	2025-12-03 23:23:58.810904	2025-12-03 23:23:58.810904
创建部门	3	1	module_system:dept:create	\N	\N	\N	\N	\N	f	t	f	创建部门	null	f	10	34	c0dc880c-d19b-481d-a0a4-9b3bcc8df987	0	初始化数据	2025-12-03 23:23:58.810907	2025-12-03 23:23:58.810907
修改部门	3	2	module_system:dept:update	\N	\N	\N	\N	\N	f	t	f	修改部门	null	f	10	35	d2c912fa-61bb-44b4-8b3d-ffec7e122705	0	初始化数据	2025-12-03 23:23:58.81091	2025-12-03 23:23:58.810911
删除部门	3	3	module_system:dept:delete	\N	\N	\N	\N	\N	f	t	f	删除部门	null	f	10	36	4d36dbae-8d1c-4f5d-862a-3bf645260f9e	0	初始化数据	2025-12-03 23:23:58.810913	2025-12-03 23:23:58.810914
批量修改部门状态	3	4	module_system:dept:patch	\N	\N	\N	\N	\N	f	t	f	批量修改部门状态	null	f	10	37	3da971f2-95cf-4424-a433-f82e1a01d3cc	0	初始化数据	2025-12-03 23:23:58.810916	2025-12-03 23:23:58.810917
创建岗位	3	1	module_system:position:create	\N	\N	\N	\N	\N	f	t	f	创建岗位	null	f	11	38	43cfe7c5-5bd6-491f-9426-8dd3dae795f1	0	初始化数据	2025-12-03 23:23:58.810919	2025-12-03 23:23:58.81092
修改岗位	3	2	module_system:position:update	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	11	39	5e0172b3-8c9b-4789-ad2e-33ce89fbe40f	0	初始化数据	2025-12-03 23:23:58.810922	2025-12-03 23:23:58.810923
删除岗位	3	3	module_system:position:delete	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	11	40	eccc20a4-a332-4712-9eea-87e85c2ca110	0	初始化数据	2025-12-03 23:23:58.810925	2025-12-03 23:23:58.810926
批量修改岗位状态	3	4	module_system:position:patch	\N	\N	\N	\N	\N	f	t	f	批量修改岗位状态	null	f	11	41	338ca31f-39ee-4bc0-98ff-0fe762138720	0	初始化数据	2025-12-03 23:23:58.810928	2025-12-03 23:23:58.810929
岗位导出	3	5	module_system:position:export	\N	\N	\N	\N	\N	f	t	f	岗位导出	null	f	11	42	82f3d790-6678-42ba-88a4-4f35e795ff77	0	初始化数据	2025-12-03 23:23:58.810931	2025-12-03 23:23:58.810932
设置角色权限	3	8	module_system:role:permission	\N	\N	\N	\N	\N	f	t	f	设置角色权限	null	f	11	43	501781a7-4224-4a6f-81da-d103b5570d16	0	初始化数据	2025-12-03 23:23:58.810934	2025-12-03 23:23:58.810935
创建角色	3	1	module_system:role:create	\N	\N	\N	\N	\N	f	t	f	创建角色	null	f	12	44	8160d56c-9a38-4678-9cdc-6126189fdeeb	0	初始化数据	2025-12-03 23:23:58.810937	2025-12-03 23:23:58.810938
修改角色	3	2	module_system:role:update	\N	\N	\N	\N	\N	f	t	f	修改角色	null	f	12	45	3da00e69-bc16-4ce2-ab3c-97d6b859f791	0	初始化数据	2025-12-03 23:23:58.81094	2025-12-03 23:23:58.810941
删除角色	3	3	module_system:role:delete	\N	\N	\N	\N	\N	f	t	f	删除角色	null	f	12	46	8cc1d822-e060-4b3f-a133-c823291b95de	0	初始化数据	2025-12-03 23:23:58.810943	2025-12-03 23:23:58.810944
批量修改角色状态	3	4	module_system:role:patch	\N	\N	\N	\N	\N	f	t	f	批量修改角色状态	null	f	12	47	a2dad3ad-c1a6-4777-bcf0-4588931a076a	0	初始化数据	2025-12-03 23:23:58.810946	2025-12-03 23:23:58.810946
角色导出	3	6	module_system:role:export	\N	\N	\N	\N	\N	f	t	f	角色导出	null	f	12	48	eae60536-fb8d-45f3-bd64-b99daceaa4fb	0	初始化数据	2025-12-03 23:23:58.810949	2025-12-03 23:23:58.810949
创建用户	3	1	module_system:user:create	\N	\N	\N	\N	\N	f	t	f	创建用户	null	f	13	49	729e5612-2cc5-4028-b0ef-0bcc6b5181be	0	初始化数据	2025-12-03 23:23:58.810952	2025-12-03 23:23:58.810953
修改用户	3	2	module_system:user:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	13	50	0ad33c79-ffb6-41c7-96e6-19baf3262c9c	0	初始化数据	2025-12-03 23:23:58.810955	2025-12-03 23:23:58.810956
删除用户	3	3	module_system:user:delete	\N	\N	\N	\N	\N	f	t	f	删除用户	null	f	13	51	d29d3284-da9c-4fc9-a131-9a6f4ac49017	0	初始化数据	2025-12-03 23:23:58.810958	2025-12-03 23:23:58.810959
批量修改用户状态	3	4	module_system:user:patch	\N	\N	\N	\N	\N	f	t	f	批量修改用户状态	null	f	13	52	6dfd4aac-1846-4ddb-af52-13e5a62e309e	0	初始化数据	2025-12-03 23:23:58.810961	2025-12-03 23:23:58.810961
导出用户	3	5	module_system:user:export	\N	\N	\N	\N	\N	f	t	f	导出用户	null	f	13	53	1a1c6883-00aa-4faf-8199-eec67444d6a7	0	初始化数据	2025-12-03 23:23:58.810964	2025-12-03 23:23:58.810964
导入用户	3	6	module_system:user:import	\N	\N	\N	\N	\N	f	t	f	导入用户	null	f	13	54	2b0ae021-a36d-4c32-891a-13bcabcd255d	0	初始化数据	2025-12-03 23:23:58.810967	2025-12-03 23:23:58.810967
日志删除	3	1	module_system:log:delete	\N	\N	\N	\N	\N	f	t	f	日志删除	null	f	14	55	4d7e3572-ec3e-4bf9-984e-3cfc232f567e	0	初始化数据	2025-12-03 23:23:58.81097	2025-12-03 23:23:58.810971
日志导出	3	2	module_system:log:export	\N	\N	\N	\N	\N	f	t	f	日志导出	null	f	14	56	80c5d203-757b-4dfd-921b-759b2c145b70	0	初始化数据	2025-12-03 23:23:58.810973	2025-12-03 23:23:58.810973
公告创建	3	1	module_system:notice:create	\N	\N	\N	\N	\N	f	t	f	公告创建	null	f	15	57	35385f33-0ef6-4f7a-b277-086c6e02b5fc	0	初始化数据	2025-12-03 23:23:58.810976	2025-12-03 23:23:58.810976
公告修改	3	2	module_system:notice:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	15	58	4ae3c260-97e1-42f6-921b-725eda3bc0b5	0	初始化数据	2025-12-03 23:23:58.810979	2025-12-03 23:23:58.810979
公告删除	3	3	module_system:notice:delete	\N	\N	\N	\N	\N	f	t	f	公告删除	null	f	15	59	ceb36c4a-f330-4f52-be9f-74d8652a21c3	0	初始化数据	2025-12-03 23:23:58.810982	2025-12-03 23:23:58.810982
公告导出	3	4	module_system:notice:export	\N	\N	\N	\N	\N	f	t	f	公告导出	null	f	15	60	1d1775cd-91e2-43cc-b2f1-e72907e1dcf5	0	初始化数据	2025-12-03 23:23:58.810985	2025-12-03 23:23:58.810985
公告批量修改状态	3	5	module_system:notice:patch	\N	\N	\N	\N	\N	f	t	f	公告批量修改状态	null	f	15	61	1a0b7abe-6268-4a37-aa6c-a0b28b022ab9	0	初始化数据	2025-12-03 23:23:58.810988	2025-12-03 23:23:58.810988
创建参数	3	1	module_system:param:create	\N	\N	\N	\N	\N	f	t	f	创建参数	null	f	16	62	e709d5f5-d02b-47be-91a9-2b1baf8a66c0	0	初始化数据	2025-12-03 23:23:58.810991	2025-12-03 23:23:58.810991
修改参数	3	2	module_system:param:update	\N	\N	\N	\N	\N	f	t	f	修改参数	null	f	16	63	1cb1d892-d635-4153-b99a-12e083703f17	0	初始化数据	2025-12-03 23:23:58.810994	2025-12-03 23:23:58.810994
删除参数	3	3	module_system:param:delete	\N	\N	\N	\N	\N	f	t	f	删除参数	null	f	16	64	10850c4c-b5bd-4f38-ae27-3f328119051a	0	初始化数据	2025-12-03 23:23:58.810997	2025-12-03 23:23:58.810997
导出参数	3	4	module_system:param:export	\N	\N	\N	\N	\N	f	t	f	导出参数	null	f	16	65	53d9dccf-b40b-4516-a95d-082b6a1b26e5	0	初始化数据	2025-12-03 23:23:58.811	2025-12-03 23:23:58.811
参数上传	3	5	module_system:param:upload	\N	\N	\N	\N	\N	f	t	f	参数上传	null	f	16	66	c6b4e368-891e-41bd-98f5-7a3c3fd8581d	0	初始化数据	2025-12-03 23:23:58.811003	2025-12-03 23:23:58.811003
创建字典类型	3	1	module_system:dict_type:create	\N	\N	\N	\N	\N	f	t	f	创建字典类型	null	f	17	67	95d270e7-acad-452c-a081-acb7ff38fb98	0	初始化数据	2025-12-03 23:23:58.811005	2025-12-03 23:23:58.811006
修改字典类型	3	2	module_system:dict_type:update	\N	\N	\N	\N	\N	f	t	f	修改字典类型	null	f	17	68	b0b6c19a-7d93-457a-b384-6f7c487b1563	0	初始化数据	2025-12-03 23:23:58.811008	2025-12-03 23:23:58.811009
删除字典类型	3	3	module_system:dict_type:delete	\N	\N	\N	\N	\N	f	t	f	删除字典类型	null	f	17	69	208a6cf0-3f93-477c-9f36-cdbc68c64905	0	初始化数据	2025-12-03 23:23:58.811011	2025-12-03 23:23:58.811012
导出字典类型	3	4	module_system:dict_type:export	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	17	70	97d21ceb-107a-478c-b9a2-d8cdbe053032	0	初始化数据	2025-12-03 23:23:58.811014	2025-12-03 23:23:58.811015
批量修改字典状态	3	5	module_system:dict_type:patch	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	17	71	438f612c-d9a3-43d7-a251-7e077975717b	0	初始化数据	2025-12-03 23:23:58.811017	2025-12-03 23:23:58.811017
字典数据查询	3	6	module_system:dict_data:query	\N	\N	\N	\N	\N	f	t	f	字典数据查询	null	f	17	72	18e90646-1d7c-4ee0-8931-9849847c1262	0	初始化数据	2025-12-03 23:23:58.81102	2025-12-03 23:23:58.81102
创建字典数据	3	7	module_system:dict_data:create	\N	\N	\N	\N	\N	f	t	f	创建字典数据	null	f	17	73	54938b41-39dd-4be8-93f5-2657ce1fe163	0	初始化数据	2025-12-03 23:23:58.811023	2025-12-03 23:23:58.811023
修改字典数据	3	8	module_system:dict_data:update	\N	\N	\N	\N	\N	f	t	f	修改字典数据	null	f	17	74	b8b55835-47d6-4c3e-8fb4-a75fc26f2b01	0	初始化数据	2025-12-03 23:23:58.811026	2025-12-03 23:23:58.811026
删除字典数据	3	9	module_system:dict_data:delete	\N	\N	\N	\N	\N	f	t	f	删除字典数据	null	f	17	75	223c4dfb-c423-40ac-8bef-f23f4b3287c5	0	初始化数据	2025-12-03 23:23:58.811029	2025-12-03 23:23:58.811029
导出字典数据	3	10	module_system:dict_data:export	\N	\N	\N	\N	\N	f	t	f	导出字典数据	null	f	17	76	4725b3b4-9307-4c12-901b-8addc9dabb89	0	初始化数据	2025-12-03 23:23:58.811032	2025-12-03 23:23:58.811032
批量修改字典数据状态	3	11	module_system:dict_data:patch	\N	\N	\N	\N	\N	f	t	f	批量修改字典数据状态	null	f	17	77	412fa6ce-123b-4cf8-aecf-303a6b6f28bf	0	初始化数据	2025-12-03 23:23:58.811035	2025-12-03 23:23:58.811035
创建应用	3	1	module_application:myapp:create	\N	\N	\N	\N	\N	f	t	f	创建应用	null	f	18	78	c52c9499-b3f0-43c0-9956-6faaf9ddb2b0	0	初始化数据	2025-12-03 23:23:58.811038	2025-12-03 23:23:58.811038
修改应用	3	2	module_application:myapp:update	\N	\N	\N	\N	\N	f	t	f	修改应用	null	f	18	79	2828ec0e-f8eb-46f4-b8df-85257f67e040	0	初始化数据	2025-12-03 23:23:58.811041	2025-12-03 23:23:58.811041
删除应用	3	3	module_application:myapp:delete	\N	\N	\N	\N	\N	f	t	f	删除应用	null	f	18	80	aa3ade39-3e53-4680-acb8-886cae652c43	0	初始化数据	2025-12-03 23:23:58.811044	2025-12-03 23:23:58.811044
批量修改应用状态	3	4	module_application:myapp:patch	\N	\N	\N	\N	\N	f	t	f	批量修改应用状态	null	f	18	81	719f76b0-9c68-4568-8d3a-a78679c7973c	0	初始化数据	2025-12-03 23:23:58.811047	2025-12-03 23:23:58.811047
创建任务	3	1	module_application:job:create	\N	\N	\N	\N	\N	f	t	f	创建任务	null	f	19	82	0208ff70-b1d4-42ca-a0c5-7a2ec429c197	0	初始化数据	2025-12-03 23:23:58.81105	2025-12-03 23:23:58.81105
修改和操作任务	3	2	module_application:job:update	\N	\N	\N	\N	\N	f	t	f	修改和操作任务	null	f	19	83	0d2ab394-c6f1-46e0-9159-c6d8fd021eba	0	初始化数据	2025-12-03 23:23:58.811053	2025-12-03 23:23:58.811053
删除和清除任务	3	3	module_application:job:delete	\N	\N	\N	\N	\N	f	t	f	删除和清除任务	null	f	19	84	cb37719a-d6e6-4f76-a7da-08ab6af975cf	0	初始化数据	2025-12-03 23:23:58.811056	2025-12-03 23:23:58.811056
导出定时任务	3	4	module_application:job:export	\N	\N	\N	\N	\N	f	t	f	导出定时任务	null	f	19	85	ad74d994-f247-4315-8e47-9a2d0e3b37fc	0	初始化数据	2025-12-03 23:23:58.811059	2025-12-03 23:23:58.811059
智能对话	3	1	module_application:ai:chat	\N	\N	\N	\N	\N	f	t	f	智能对话	null	f	20	86	2f2dc701-9dc4-4a67-a1b2-dc79ac8d4688	0	智能对话	2025-12-03 23:23:58.811062	2025-12-03 23:23:58.811062
在线用户强制下线	3	1	module_monitor:online:delete	\N	\N	\N	\N	\N	f	f	f	在线用户强制下线	null	f	22	87	47bca5dd-c9ef-4fa5-a13a-9bd5edd10fdd	0	初始化数据	2025-12-03 23:23:58.811065	2025-12-03 23:23:58.811065
清除缓存	3	1	module_monitor:cache:delete	\N	\N	\N	\N	\N	f	f	f	清除缓存	null	f	24	88	a66c47cb-35b6-47da-98fc-bdd95cac1d13	0	初始化数据	2025-12-03 23:23:58.811067	2025-12-03 23:23:58.811068
文件上传	3	1	module_monitor:resource:upload	\N	\N	\N	\N	\N	f	t	f	文件上传	null	f	25	89	27112be6-014c-4f03-9e31-34db8f86c077	0	初始化数据	2025-12-03 23:23:58.81107	2025-12-03 23:23:58.811071
文件下载	3	2	module_monitor:resource:download	\N	\N	\N	\N	\N	f	t	f	文件下载	null	f	25	90	3f5e895a-7a09-47c8-877f-7d0d9279e796	0	初始化数据	2025-12-03 23:23:58.811073	2025-12-03 23:23:58.811074
文件删除	3	3	module_monitor:resource:delete	\N	\N	\N	\N	\N	f	t	f	文件删除	null	f	25	91	de8a3457-ffa3-4a0c-b019-4c4ddc739d20	0	初始化数据	2025-12-03 23:23:58.811076	2025-12-03 23:23:58.811077
文件移动	3	4	module_monitor:resource:move	\N	\N	\N	\N	\N	f	t	f	文件移动	null	f	25	92	1a583db4-906d-4f6a-b5a8-f06f8718f284	0	初始化数据	2025-12-03 23:23:58.811079	2025-12-03 23:23:58.81108
文件复制	3	5	module_monitor:resource:copy	\N	\N	\N	\N	\N	f	t	f	文件复制	null	f	25	93	41c7d0f1-c0e7-4366-8de4-790226ea4790	0	初始化数据	2025-12-03 23:23:58.811082	2025-12-03 23:23:58.811083
文件重命名	3	6	module_monitor:resource:rename	\N	\N	\N	\N	\N	f	t	f	文件重命名	null	f	25	94	b831c56c-9f55-4f2a-ad03-3e6fd32d143f	0	初始化数据	2025-12-03 23:23:58.811085	2025-12-03 23:23:58.811086
创建目录	3	7	module_monitor:resource:create_dir	\N	\N	\N	\N	\N	f	t	f	创建目录	null	f	25	95	e6afcdb4-eb8c-4915-b9a5-16e4b2f78421	0	初始化数据	2025-12-03 23:23:58.811088	2025-12-03 23:23:58.811089
导出文件列表	3	9	module_monitor:resource:export	\N	\N	\N	\N	\N	f	t	f	导出文件列表	null	f	25	96	6eb9ec7e-b64e-41a2-9752-5d7078ec986d	0	初始化数据	2025-12-03 23:23:58.811091	2025-12-03 23:23:58.811091
查询代码生成业务表列表	3	1	module_generator:gencode:query	\N	\N	\N	\N	\N	f	t	f	查询代码生成业务表列表	null	f	26	97	c53586c3-a7ca-4d93-a143-9c50f8693385	0	查询代码生成业务表列表	2025-12-03 23:23:58.811094	2025-12-03 23:23:58.811094
创建表结构	3	2	module_generator:gencode:create	\N	\N	\N	\N	\N	f	t	f	创建表结构	null	f	26	98	ac95cea8-e27a-4082-a5f4-6e7cf30f3dc8	0	创建表结构	2025-12-03 23:23:58.811097	2025-12-03 23:23:58.811097
编辑业务表信息	3	3	module_generator:gencode:update	\N	\N	\N	\N	\N	f	t	f	编辑业务表信息	null	f	26	99	fb110aae-f963-418b-9a5b-d7d354d99faf	0	编辑业务表信息	2025-12-03 23:23:58.8111	2025-12-03 23:23:58.8111
删除业务表信息	3	4	module_generator:gencode:delete	\N	\N	\N	\N	\N	f	t	f	删除业务表信息	null	f	26	100	a4e1ce58-8ea7-4259-bbac-352dd05bd720	0	删除业务表信息	2025-12-03 23:23:58.811103	2025-12-03 23:23:58.811103
导入表结构	3	5	module_generator:gencode:import	\N	\N	\N	\N	\N	f	t	f	导入表结构	null	f	26	101	f1602bc5-46fc-438b-aa65-74be1c47de53	0	导入表结构	2025-12-03 23:23:58.811106	2025-12-03 23:23:58.811106
批量生成代码	3	6	module_generator:gencode:operate	\N	\N	\N	\N	\N	f	t	f	批量生成代码	null	f	26	102	ffc99866-fa60-4629-ad17-1a551ac15caa	0	批量生成代码	2025-12-03 23:23:58.811109	2025-12-03 23:23:58.811109
生成代码到指定路径	3	7	module_generator:gencode:code	\N	\N	\N	\N	\N	f	t	f	生成代码到指定路径	null	f	26	103	b26f1689-2040-4ee8-9d38-4d70e21e177d	0	生成代码到指定路径	2025-12-03 23:23:58.811112	2025-12-03 23:23:58.811112
查询数据库表列表	3	8	module_generator:dblist:query	\N	\N	\N	\N	\N	f	t	f	查询数据库表列表	null	f	26	104	b12ca981-57f3-48c9-abe5-8f021379260b	0	查询数据库表列表	2025-12-03 23:23:58.811115	2025-12-03 23:23:58.811115
同步数据库	3	9	module_generator:db:sync	\N	\N	\N	\N	\N	f	t	f	同步数据库	null	f	26	105	f2695e07-46e6-4474-ba3c-2423985b393b	0	同步数据库	2025-12-03 23:23:58.811118	2025-12-03 23:23:58.811118
创建示例	3	1	module_gencode:demo:create	\N	\N	\N	\N	\N	f	t	f	创建示例	null	f	29	106	0765e72d-cc91-49b9-bdc5-147868f00f1e	0	初始化数据	2025-12-03 23:23:58.811121	2025-12-03 23:23:58.811121
更新示例	3	2	module_gencode:demo:update	\N	\N	\N	\N	\N	f	t	f	更新示例	null	f	29	107	0d9973c9-bf73-4f8a-a0c8-0b7477e955c5	0	初始化数据	2025-12-03 23:23:58.811124	2025-12-03 23:23:58.811124
删除示例	3	3	module_gencode:demo:delete	\N	\N	\N	\N	\N	f	t	f	删除示例	null	f	29	108	c10732c4-7d4d-4a18-b55a-e879915e7821	0	初始化数据	2025-12-03 23:23:58.811127	2025-12-03 23:23:58.811127
批量修改示例状态	3	4	module_gencode:demo:patch	\N	\N	\N	\N	\N	f	t	f	批量修改示例状态	null	f	29	109	46a710af-cc8a-4c84-8628-cfecde988dd9	0	初始化数据	2025-12-03 23:23:58.81113	2025-12-03 23:23:58.81113
导出示例	3	5	module_gencode:demo:export	\N	\N	\N	\N	\N	f	t	f	导出示例	null	f	29	110	64ca18eb-01c8-492c-a828-2beae7805de5	0	初始化数据	2025-12-03 23:23:58.811133	2025-12-03 23:23:58.811133
导入示例	3	6	module_gencode:demo:import	\N	\N	\N	\N	\N	f	t	f	导入示例	null	f	29	111	b83aa5af-9acc-43a8-874f-b5042ac10875	0	初始化数据	2025-12-03 23:23:58.811136	2025-12-03 23:23:58.811136
下载导入示例模版	3	7	module_gencode:demo:download	\N	\N	\N	\N	\N	f	t	f	下载导入示例模版	null	f	29	112	9a32c6b9-705b-45f5-92d8-583d7dca1b96	0	初始化数据	2025-12-03 23:23:58.811139	2025-12-03 23:23:58.811139
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
网站名称	sys_web_title	FastApiAdmin	t	1	c05e093f-af86-4a84-b090-f1a260afe2c6	0	初始化数据	2025-12-03 23:23:58.817316	2025-12-03 23:23:58.817316
网站描述	sys_web_description	FastApiAdmin 是完全开源的权限管理系统	t	2	b2b531a6-8164-4205-b2a1-b786807e3220	0	初始化数据	2025-12-03 23:23:58.81732	2025-12-03 23:23:58.817321
网页图标	sys_web_favicon	https://service.fastapiadmin.com/api/v1/static/image/favicon.png	t	3	a5cc723e-b6d3-4f60-ac73-bda6b9144a7b	0	初始化数据	2025-12-03 23:23:58.817324	2025-12-03 23:23:58.817324
网站Logo	sys_web_logo	https://service.fastapiadmin.com/api/v1/static/image/logo.png	t	4	67a2dad5-26a0-4b56-9ba5-19606f3acbe4	0	初始化数据	2025-12-03 23:23:58.817327	2025-12-03 23:23:58.817327
登录背景	sys_login_background	https://service.fastapiadmin.com/api/v1/static/image/background.svg	t	5	d950b25d-ab42-4785-8816-6ba10c5537b0	0	初始化数据	2025-12-03 23:23:58.81733	2025-12-03 23:23:58.81733
版权信息	sys_web_copyright	Copyright © 2025-2026 service.fastapiadmin.com 版权所有	t	6	bfd17119-2d6b-4a91-9c94-682c1aa7621e	0	初始化数据	2025-12-03 23:23:58.817333	2025-12-03 23:23:58.817333
备案信息	sys_keep_record	陕ICP备2025069493号-1	t	7	92730d60-fdcb-4d9d-b4cd-de1456966e95	0	初始化数据	2025-12-03 23:23:58.817336	2025-12-03 23:23:58.817336
帮助文档	sys_help_doc	https://service.fastapiadmin.com	t	8	5548caa0-4be2-4fc1-a2ba-1149a7d4df20	0	初始化数据	2025-12-03 23:23:58.817339	2025-12-03 23:23:58.817339
隐私政策	sys_web_privacy	https://github.com/1014TaoTao/FastapiAdmin/blob/master/LICENSE	t	9	c54afbf9-e545-48e9-8261-87cc65f201f8	0	初始化数据	2025-12-03 23:23:58.817342	2025-12-03 23:23:58.817342
用户协议	sys_web_clause	https://github.com/1014TaoTao/FastapiAdmin/blob/master/LICENSE	t	10	4f6279ae-d1e9-446a-b6ac-30ea74a99b19	0	初始化数据	2025-12-03 23:23:58.817345	2025-12-03 23:23:58.817345
源码代码	sys_git_code	https://github.com/1014TaoTao/FastapiAdmin.git	t	11	97d2c838-0828-4827-9185-cb543683d460	0	初始化数据	2025-12-03 23:23:58.817348	2025-12-03 23:23:58.817348
项目版本	sys_web_version	2.0.0	t	12	2630675b-71c7-4417-b334-aec5b73a3680	0	初始化数据	2025-12-03 23:23:58.817351	2025-12-03 23:23:58.817351
演示模式启用	demo_enable	false	t	13	03775492-3475-4ccd-9009-c1d8730d55ca	0	初始化数据	2025-12-03 23:23:58.817354	2025-12-03 23:23:58.817354
演示访问IP白名单	ip_white_list	["127.0.0.1"]	t	14	fcf49a0c-7bc9-413e-8cb2-6e11b5af1db4	0	初始化数据	2025-12-03 23:23:58.817357	2025-12-03 23:23:58.817357
接口白名单	white_api_list_path	["/api/v1/system/auth/login", "/api/v1/system/auth/token/refresh", "/api/v1/system/auth/captcha/get", "/api/v1/system/auth/logout", "/api/v1/system/config/info", "/api/v1/system/user/current/info", "/api/v1/system/notice/available"]	t	15	0f3cc21a-3d1e-436c-9eb6-3624ac430ca8	0	初始化数据	2025-12-03 23:23:58.81736	2025-12-03 23:23:58.81736
访问IP黑名单	ip_black_list	[]	t	16	7f3b2e72-df33-45a5-bc5a-a6533b43c96d	0	初始化数据	2025-12-03 23:23:58.817363	2025-12-03 23:23:58.817363
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
管理员角色	ADMIN	1	4	1	f775fc7c-2643-4feb-a647-182f293b7952	0	初始化角色	2025-12-03 23:23:58.825334	2025-12-03 23:23:58.825335
仅个人数据	MINE	1	1	2	242f44f5-6faf-4245-aac7-482630ddb6f7	0	\N	2025-12-04 21:22:35.101163	2025-12-04 21:29:46.636526
本部门数据	DEPT	1	2	4	6a229f0d-7dcb-4b66-9054-987e3c1dfe5d	0	\N	2025-12-04 21:23:30.471024	2025-12-04 21:29:59.097303
本部门及以下	ALL_DEPT	1	3	5	b419c2ef-af62-4d93-80e5-4afb24be9289	0	\N	2025-12-04 21:23:50.681785	2025-12-04 21:30:14.524507
全部数据	ALL	1	4	3	91131798-462f-498a-a4c8-e2df5f8ebdb6	0	\N	2025-12-04 21:23:11.221725	2025-12-04 21:30:37.290914
自定义数据	ZIDINGYI	1	5	6	96f6a404-d6b0-4a46-b6fa-5cbd56e42739	0	\N	2025-12-04 21:32:02.7182	2025-12-04 22:10:03.370597
\.


--
-- Data for Name: sys_role_depts; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_role_depts (role_id, dept_id) FROM stdin;
2	4
2	5
2	2
2	3
2	1
2	6
2	7
4	5
4	4
4	6
4	2
4	7
4	1
4	3
5	6
5	1
5	3
5	4
5	7
5	5
5	2
3	3
3	7
3	1
3	6
3	4
3	5
3	2
6	2
\.


--
-- Data for Name: sys_role_menus; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_role_menus (role_id, menu_id) FROM stdin;
2	109
2	107
2	108
2	111
2	7
2	110
2	112
2	106
2	29
4	7
4	29
4	107
4	108
4	110
4	111
4	106
4	109
4	112
5	29
5	107
5	112
5	106
5	109
5	7
5	108
5	111
5	110
3	107
3	29
3	111
3	7
3	110
3	108
3	109
3	106
3	112
6	106
6	107
6	109
6	110
6	112
6	108
6	7
6	29
6	111
\.


--
-- Data for Name: sys_user; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_user (username, password, name, mobile, email, gender, avatar, is_superuser, last_login, gitee_login, github_login, wx_login, qq_login, dept_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
test22	$2b$12$/0pNNfFW1n3dEJAnPxe6LOmodfU1zHbPmUGsNPOW1ucOOOUbEAHVm	本部门数据2	\N	\N	2	\N	f	2025-12-04 14:06:37.659308+00	\N	\N	\N	\N	3	8	795f3692-ad0c-44ea-8e36-4bcb6c4dd957	0	\N	2025-12-04 22:06:19.287286	2025-12-04 22:06:37.69025	1	1
test2	$2b$12$VF1IjpXM1/Y604M4QE509OqtVHbTaEBkmPO0WfWxEqzm1gdveDBNi	本部门数据	\N	\N	2	\N	f	2025-12-04 14:07:10.846327+00	\N	\N	\N	\N	3	3	4c2b0473-3130-4c4d-bebf-94412ea05c7e	0	\N	2025-12-04 21:41:18.554796	2025-12-04 22:07:10.877735	1	1
test1	$2b$12$GnAIyhOri8fJjgoCLRUTVOovW6bfIXLdRPh0YYE5RcV3bKdJgVz1S	本部门及以下	\N	\N	2	\N	f	2025-12-04 14:08:15.28931+00	\N	\N	\N	\N	2	2	3ad9aac5-c7e8-49dd-8bc0-ba42660dfa29	0	\N	2025-12-03 23:24:32.770483	2025-12-04 22:08:15.324536	1	1
test1_1	$2b$12$M/KNhjFGMdr0nm0HmZm7JeEc3eb8PZKkX1WCgsqZq.z0Gju6J7UG6	全部数据	\N	\N	2	\N	f	2025-12-04 14:08:38.530361+00	\N	\N	\N	\N	4	4	0164b4be-69e8-437e-9b37-87727eae3964	0	\N	2025-12-04 21:41:51.147687	2025-12-04 22:08:38.560298	1	1
admin	$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa	超级管理员	\N	\N	0	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	t	2025-12-04 14:09:08.017972+00	\N	\N	\N	\N	1	1	5e8d00aa-2b53-409d-88df-82e713f2360d	0	超级管理员	2025-12-03 23:23:58.837235	2025-12-04 22:09:08.030298	\N	\N
test2_1	$2b$12$QaSuhXtbd32TclDQX.sle.rW2ByUM36ld0t46psEEbYKRIFLiZxWu	自定义1	\N	\N	2	\N	f	2025-12-04 14:10:45.546955+00	\N	\N	\N	\N	7	6	46f2a531-af05-423f-a504-cee642327336	0	\N	2025-12-04 21:46:20.511536	2025-12-04 22:10:45.5783	1	1
test2_2	$2b$12$7VjR260GghaKx1BOczedTumXlsdab1iCSt4SiySCwUniAY8XcxAZu	test2_2	\N	\N	2	\N	f	2025-12-04 13:50:36.078774+00	\N	\N	\N	\N	6	7	da0c4cec-c428-4347-ba67-ec6b1878fc2c	0	\N	2025-12-04 21:46:42.948817	2025-12-04 22:02:26.511693	1	1
test1_2	$2b$12$ZW6BK1WCEepwRgevC/.9n.TnSwsftYa9tYOiWpiuUEIcFE045Z5ma	仅个人	\N	\N	2	\N	f	2025-12-04 14:03:21.792954+00	\N	\N	\N	\N	5	5	b730fcb1-2cff-472c-9809-a4167313e6fb	0	\N	2025-12-04 21:44:44.234721	2025-12-04 22:03:21.826152	1	1
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
4	3
7	3
3	4
2	5
5	2
6	6
8	4
\.


--
-- Name: app_ai_mcp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.app_ai_mcp_id_seq', 1, false);


--
-- Name: app_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.app_job_id_seq', 1, false);


--
-- Name: app_job_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.app_job_log_id_seq', 1, false);


--
-- Name: app_myapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.app_myapp_id_seq', 1, false);


--
-- Name: gen_demo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_demo_id_seq', 9, true);


--
-- Name: gen_table_column_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_table_column_id_seq', 9, true);


--
-- Name: gen_table_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_table_id_seq', 1, true);


--
-- Name: sys_dept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_dept_id_seq', 7, true);


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

SELECT pg_catalog.setval('public.sys_log_id_seq', 103, true);


--
-- Name: sys_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_menu_id_seq', 112, true);


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

SELECT pg_catalog.setval('public.sys_role_id_seq', 6, true);


--
-- Name: sys_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_user_id_seq', 8, true);


--
-- Name: app_ai_mcp app_ai_mcp_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_ai_mcp
    ADD CONSTRAINT app_ai_mcp_pkey PRIMARY KEY (id);


--
-- Name: app_ai_mcp app_ai_mcp_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_ai_mcp
    ADD CONSTRAINT app_ai_mcp_uuid_key UNIQUE (uuid);


--
-- Name: app_job_log app_job_log_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job_log
    ADD CONSTRAINT app_job_log_pkey PRIMARY KEY (id);


--
-- Name: app_job_log app_job_log_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job_log
    ADD CONSTRAINT app_job_log_uuid_key UNIQUE (uuid);


--
-- Name: app_job app_job_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job
    ADD CONSTRAINT app_job_pkey PRIMARY KEY (id);


--
-- Name: app_job app_job_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job
    ADD CONSTRAINT app_job_uuid_key UNIQUE (uuid);


--
-- Name: app_myapp app_myapp_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_myapp
    ADD CONSTRAINT app_myapp_pkey PRIMARY KEY (id);


--
-- Name: app_myapp app_myapp_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_myapp
    ADD CONSTRAINT app_myapp_uuid_key UNIQUE (uuid);


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
-- Name: gen_demo gen_demo_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_demo
    ADD CONSTRAINT gen_demo_uuid_key UNIQUE (uuid);


--
-- Name: gen_table_column gen_table_column_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_pkey PRIMARY KEY (id);


--
-- Name: gen_table_column gen_table_column_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_uuid_key UNIQUE (uuid);


--
-- Name: gen_table gen_table_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_pkey PRIMARY KEY (id);


--
-- Name: gen_table gen_table_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_uuid_key UNIQUE (uuid);


--
-- Name: sys_dept sys_dept_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_pkey PRIMARY KEY (id);


--
-- Name: sys_dept sys_dept_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_uuid_key UNIQUE (uuid);


--
-- Name: sys_dict_data sys_dict_data_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_pkey PRIMARY KEY (id);


--
-- Name: sys_dict_data sys_dict_data_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_uuid_key UNIQUE (uuid);


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
-- Name: sys_dict_type sys_dict_type_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_type
    ADD CONSTRAINT sys_dict_type_uuid_key UNIQUE (uuid);


--
-- Name: sys_log sys_log_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_pkey PRIMARY KEY (id);


--
-- Name: sys_log sys_log_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_uuid_key UNIQUE (uuid);


--
-- Name: sys_menu sys_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_menu
    ADD CONSTRAINT sys_menu_pkey PRIMARY KEY (id);


--
-- Name: sys_menu sys_menu_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_menu
    ADD CONSTRAINT sys_menu_uuid_key UNIQUE (uuid);


--
-- Name: sys_notice sys_notice_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_pkey PRIMARY KEY (id);


--
-- Name: sys_notice sys_notice_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_uuid_key UNIQUE (uuid);


--
-- Name: sys_param sys_param_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_param
    ADD CONSTRAINT sys_param_pkey PRIMARY KEY (id);


--
-- Name: sys_param sys_param_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_param
    ADD CONSTRAINT sys_param_uuid_key UNIQUE (uuid);


--
-- Name: sys_position sys_position_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_pkey PRIMARY KEY (id);


--
-- Name: sys_position sys_position_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_uuid_key UNIQUE (uuid);


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
-- Name: sys_role sys_role_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role
    ADD CONSTRAINT sys_role_uuid_key UNIQUE (uuid);


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
-- Name: sys_user sys_user_uuid_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_uuid_key UNIQUE (uuid);


--
-- Name: ix_app_ai_mcp_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_ai_mcp_created_id ON public.app_ai_mcp USING btree (created_id);


--
-- Name: ix_app_ai_mcp_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_ai_mcp_updated_id ON public.app_ai_mcp USING btree (updated_id);


--
-- Name: ix_app_job_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_created_id ON public.app_job USING btree (created_id);


--
-- Name: ix_app_job_log_job_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_log_job_id ON public.app_job_log USING btree (job_id);


--
-- Name: ix_app_job_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_updated_id ON public.app_job USING btree (updated_id);


--
-- Name: ix_app_myapp_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_created_id ON public.app_myapp USING btree (created_id);


--
-- Name: ix_app_myapp_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_updated_id ON public.app_myapp USING btree (updated_id);


--
-- Name: ix_apscheduler_jobs_next_run_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_apscheduler_jobs_next_run_time ON public.apscheduler_jobs USING btree (next_run_time);


--
-- Name: ix_gen_demo_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_created_id ON public.gen_demo USING btree (created_id);


--
-- Name: ix_gen_demo_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_updated_id ON public.gen_demo USING btree (updated_id);


--
-- Name: ix_gen_table_column_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_created_id ON public.gen_table_column USING btree (created_id);


--
-- Name: ix_gen_table_column_table_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_table_id ON public.gen_table_column USING btree (table_id);


--
-- Name: ix_gen_table_column_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_updated_id ON public.gen_table_column USING btree (updated_id);


--
-- Name: ix_gen_table_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_created_id ON public.gen_table USING btree (created_id);


--
-- Name: ix_gen_table_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_updated_id ON public.gen_table USING btree (updated_id);


--
-- Name: ix_sys_dept_code; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_code ON public.sys_dept USING btree (code);


--
-- Name: ix_sys_dept_parent_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_parent_id ON public.sys_dept USING btree (parent_id);


--
-- Name: ix_sys_log_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_created_id ON public.sys_log USING btree (created_id);


--
-- Name: ix_sys_log_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_updated_id ON public.sys_log USING btree (updated_id);


--
-- Name: ix_sys_menu_parent_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_parent_id ON public.sys_menu USING btree (parent_id);


--
-- Name: ix_sys_notice_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_created_id ON public.sys_notice USING btree (created_id);


--
-- Name: ix_sys_notice_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_updated_id ON public.sys_notice USING btree (updated_id);


--
-- Name: ix_sys_position_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_created_id ON public.sys_position USING btree (created_id);


--
-- Name: ix_sys_position_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_updated_id ON public.sys_position USING btree (updated_id);


--
-- Name: ix_sys_role_code; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_code ON public.sys_role USING btree (code);


--
-- Name: ix_sys_user_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_created_id ON public.sys_user USING btree (created_id);


--
-- Name: ix_sys_user_dept_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_dept_id ON public.sys_user USING btree (dept_id);


--
-- Name: ix_sys_user_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_updated_id ON public.sys_user USING btree (updated_id);


--
-- Name: app_ai_mcp app_ai_mcp_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_ai_mcp
    ADD CONSTRAINT app_ai_mcp_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_ai_mcp app_ai_mcp_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_ai_mcp
    ADD CONSTRAINT app_ai_mcp_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_job app_job_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job
    ADD CONSTRAINT app_job_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_job_log app_job_log_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job_log
    ADD CONSTRAINT app_job_log_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.app_job(id) ON DELETE CASCADE;


--
-- Name: app_job app_job_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job
    ADD CONSTRAINT app_job_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


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
-- PostgreSQL database dump complete
--

