import type { ColDef, SqlDialect, VisualBuildState } from './buildCreateTableSql';

/** 与代码生成第三步「基本信息」联动时的输入（主表名、子表名、外键列名） */
export interface GenTableCreateLink {
  table_name?: string;
  table_comment?: string;
  sub_table_name?: string;
  sub_table_fk_name?: string;
}

function mixinMysql(): ColDef[] {
  return [
    {
      name: 'status',
      type: 'varchar(10)',
      nullable: false,
      isPk: false,
      comment: '是否启用(0:启用 1:禁用)',
    },
    { name: 'description', type: 'text', nullable: true, isPk: false, comment: '备注/描述' },
    {
      name: 'created_time',
      type: 'datetime',
      nullable: false,
      isPk: false,
      comment: '创建时间',
    },
    {
      name: 'updated_time',
      type: 'datetime',
      nullable: false,
      isPk: false,
      comment: '更新时间',
    },
    { name: 'created_id', type: 'int', nullable: true, isPk: false, comment: '创建人ID' },
    { name: 'updated_id', type: 'int', nullable: true, isPk: false, comment: '更新人ID' },
    {
      name: 'is_deleted',
      type: 'tinyint(1)',
      nullable: false,
      isPk: false,
      comment: '是否已删除(0:未删除 1:已删除)',
    },
    { name: 'deleted_time', type: 'datetime', nullable: true, isPk: false, comment: '删除时间' },
    { name: 'deleted_id', type: 'int', nullable: true, isPk: false, comment: '删除人ID' },
  ];
}

function mixinPostgres(): ColDef[] {
  return [
    {
      name: 'status',
      type: 'varchar(10)',
      nullable: false,
      isPk: false,
      comment: '是否启用(0:启用 1:禁用)',
    },
    { name: 'description', type: 'text', nullable: true, isPk: false, comment: '备注/描述' },
    {
      name: 'created_time',
      type: 'timestamp without time zone',
      nullable: false,
      isPk: false,
      comment: '创建时间',
    },
    {
      name: 'updated_time',
      type: 'timestamp without time zone',
      nullable: false,
      isPk: false,
      comment: '更新时间',
    },
    { name: 'created_id', type: 'integer', nullable: true, isPk: false, comment: '创建人ID' },
    { name: 'updated_id', type: 'integer', nullable: true, isPk: false, comment: '更新人ID' },
    {
      name: 'is_deleted',
      type: 'boolean',
      nullable: false,
      isPk: false,
      comment: '是否已删除(0:未删除 1:已删除)',
    },
    {
      name: 'deleted_time',
      type: 'timestamp without time zone',
      nullable: true,
      isPk: false,
      comment: '删除时间',
    },
    { name: 'deleted_id', type: 'integer', nullable: true, isPk: false, comment: '删除人ID' },
  ];
}

function pkMysql(): ColDef[] {
  return [
    {
      name: 'id',
      type: 'bigint',
      nullable: false,
      isPk: true,
      comment: '主键ID',
      autoIncrement: true,
    },
    {
      name: 'uuid',
      type: 'varchar(64)',
      nullable: false,
      isPk: false,
      comment: 'UUID全局唯一标识',
    },
  ];
}

function pkPostgres(): ColDef[] {
  return [
    { name: 'id', type: 'SERIAL', nullable: false, isPk: true, comment: '主键ID' },
    {
      name: 'uuid',
      type: 'varchar(64)',
      nullable: false,
      isPk: false,
      comment: 'UUID全局唯一标识',
    },
  ];
}

function buildSubColumns(dialect: SqlDialect, mainTableName: string, fkColumn: string): ColDef[] {
  const isMysql = dialect === 'mysql';
  const mixin = isMysql ? mixinMysql() : mixinPostgres();
  const subPk = isMysql ? pkMysql() : pkPostgres();
  const fkColDef: ColDef = {
    name: fkColumn,
    type: 'bigint',
    nullable: false,
    isPk: false,
    comment: `关联 ${mainTableName}.${'id'}`,
  };
  const subBusiness: ColDef[] = [
    {
      name: 'line_name',
      type: 'varchar(128)',
      nullable: true,
      isPk: false,
      comment: '明细名称',
    },
    {
      name: 'qty',
      type: isMysql ? 'int' : 'integer',
      nullable: false,
      isPk: false,
      comment: '数量',
    },
  ];
  return [...subPk, fkColDef, ...subBusiness, ...mixin];
}

export function applySubColumns(state: VisualBuildState): VisualBuildState {
  if (!state.subEnabled) {
    return { ...state, subColumns: [] };
  }
  return {
    ...state,
    subColumns: buildSubColumns(state.dialect, state.mainTableName, state.fkColumn),
  };
}

/** 单表：带业务字段 name */
export function visualPresetSingle(dialect: SqlDialect): VisualBuildState {
  const isMysql = dialect === 'mysql';
  const mixin = isMysql ? mixinMysql() : mixinPostgres();
  const pk = isMysql ? pkMysql() : pkPostgres();
  const business: ColDef[] = [
    { name: 'name', type: 'varchar(64)', nullable: true, isPk: false, comment: '名称' },
  ];
  return {
    dialect,
    mainTableName: 'gen_demo_single',
    mainComment: '代码生成-单表示例',
    mainColumns: [...pk, ...business, ...mixin],
    subEnabled: false,
    subTableName: 'gen_demo_order_item',
    subComment: '子表示例',
    fkColumn: 'order_id',
    fkRefColumn: 'id',
    subColumns: [],
  };
}

/** 主子表：主表订单头 + 子表明细，子表含外键列 */
export function visualPresetMasterSub(dialect: SqlDialect): VisualBuildState {
  const isMysql = dialect === 'mysql';
  const mixin = isMysql ? mixinMysql() : mixinPostgres();
  const pk = isMysql ? pkMysql() : pkPostgres();
  const mainBusiness: ColDef[] = [
    {
      name: 'order_title',
      type: 'varchar(128)',
      nullable: true,
      isPk: false,
      comment: '订单标题',
    },
  ];
  return applySubColumns({
    dialect,
    mainTableName: 'gen_demo_order_master',
    mainComment: '代码生成-主表示例（订单头）',
    mainColumns: [...pk, ...mainBusiness, ...mixin],
    subEnabled: true,
    subTableName: 'gen_demo_order_item',
    subComment: '代码生成-子表示例（订单明细）',
    fkColumn: 'order_id',
    fkRefColumn: 'id',
    subColumns: [],
  });
}

/**
 * 将第三步已填的主子表信息合并到表结构预设。
 * 规则：子表名与外键列名同时非空时使用主子表模板；否则为单表模板（仅主表名/注释覆盖）。
 */
export function mergeGenTableLinkIntoVisual(
  link: GenTableCreateLink,
  dialect: SqlDialect
): VisualBuildState {
  const main = (link.table_name || '').trim();
  const subSn = (link.sub_table_name || '').trim();
  const subFk = (link.sub_table_fk_name || '').trim();
  const hasSubPair = Boolean(subSn && subFk);
  const base: VisualBuildState = hasSubPair
    ? visualPresetMasterSub(dialect)
    : visualPresetSingle(dialect);
  if (main) base.mainTableName = main;
  const mc = (link.table_comment || '').trim();
  if (mc) base.mainComment = mc;
  if (hasSubPair) {
    base.subEnabled = true;
    base.subTableName = subSn;
    base.fkColumn = subFk;
    base.fkRefColumn = 'id';
  } else {
    base.subEnabled = false;
  }
  return applySubColumns(base);
}
