/**
 * 将「表结构」表单状态编译为可执行的 CREATE TABLE SQL（MySQL / PostgreSQL）。
 */

export type SqlDialect = "mysql" | "postgres";

export interface ColDef {
  name: string;
  type: string;
  nullable: boolean;
  isPk: boolean;
  comment: string;
  /** 仅 MySQL：数字主键自增 */
  autoIncrement?: boolean;
}

export interface VisualBuildState {
  dialect: SqlDialect;
  mainTableName: string;
  mainComment: string;
  mainColumns: ColDef[];
  subEnabled: boolean;
  subTableName: string;
  subComment: string;
  /** 子表上指向主表的外键列名 */
  fkColumn: string;
  /** 主表被引用列，一般为 id */
  fkRefColumn: string;
  subColumns: ColDef[];
}

function qMysql(name: string): string {
  return `\`${name.replace(/`/g, "")}\``;
}

function buildMysqlTable(name: string, comment: string, columns: ColDef[]): string {
  const lines: string[] = [];
  const pkCols = columns.filter((c) => c.isPk).map((c) => qMysql(c.name));
  for (const c of columns) {
    let line = `  ${qMysql(c.name)} ${c.type}`;
    if (c.isPk && c.autoIncrement) {
      line += " NOT NULL AUTO_INCREMENT";
    } else if (c.isPk) {
      line += " NOT NULL";
    } else if (!c.nullable) {
      line += " NOT NULL";
    } else {
      line += " DEFAULT NULL";
    }
    if (c.comment) line += ` COMMENT '${c.comment.replace(/'/g, "''")}'`;
    lines.push(line);
  }
  const tail: string[] = [];
  if (pkCols.length) {
    tail.push(`  PRIMARY KEY (${pkCols.join(", ")})`);
  }
  const uuidCol = columns.find((c) => c.name === "uuid");
  if (uuidCol) {
    tail.push(`  UNIQUE KEY ${qMysql(`uk_${name.replace(/`/g, "")}_uuid`)} (${qMysql("uuid")})`);
  }
  const allLines = [...lines, ...tail];
  return (
    `CREATE TABLE ${qMysql(name)} (\n${allLines.join(",\n")}\n)` +
    ` ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='${comment.replace(/'/g, "''")}';`
  );
}

function buildMysqlFk(subName: string, fkCol: string, mainName: string, refCol: string): string {
  return (
    `ALTER TABLE ${qMysql(subName)} ADD CONSTRAINT ${qMysql(`fk_${subName}_${fkCol}`)} ` +
    `FOREIGN KEY (${qMysql(fkCol)}) REFERENCES ${qMysql(mainName)} (${qMysql(refCol)}) ON DELETE CASCADE;`
  );
}

function buildPostgresTable(name: string, comment: string, columns: ColDef[]): string {
  const lines: string[] = [];
  const pkCols = columns.filter((c) => c.isPk).map((c) => c.name);
  for (const c of columns) {
    let line = `  ${c.name} ${c.type}`;
    const isSerial = c.type.toUpperCase().includes("SERIAL");
    if (!isSerial && !c.nullable) line += " NOT NULL";
    lines.push(line);
  }
  const tail: string[] = [];
  if (pkCols.length) {
    tail.push(`  PRIMARY KEY (${pkCols.join(", ")})`);
  }
  const body = [...lines, ...tail].join(",\n");
  return (
    `CREATE TABLE ${name} (\n${body}\n);\n` +
    `COMMENT ON TABLE ${name} IS '${comment.replace(/'/g, "''")}';`
  );
}

function buildPostgresColumnComments(table: string, columns: ColDef[]): string {
  return columns
    .filter((c) => c.comment)
    .map((c) => `COMMENT ON COLUMN ${table}.${c.name} IS '${c.comment.replace(/'/g, "''")}';`)
    .join("\n");
}

function buildPostgresFk(subName: string, fkCol: string, mainName: string, refCol: string): string {
  return (
    `ALTER TABLE ${subName} ADD CONSTRAINT fk_${subName}_${fkCol} ` +
    `FOREIGN KEY (${fkCol}) REFERENCES ${mainName}(${refCol}) ON DELETE CASCADE;`
  );
}

/** 由表结构状态生成完整 SQL（单表或主子表） */
export function buildSqlFromVisual(state: VisualBuildState): string {
  const m = state.mainTableName.trim();
  if (!m) return "";

  const parts: string[] = [];

  if (state.dialect === "mysql") {
    parts.push(buildMysqlTable(m, state.mainComment || m, state.mainColumns));
    if (state.subEnabled && state.subTableName.trim()) {
      const s = state.subTableName.trim();
      parts.push(buildMysqlTable(s, state.subComment || s, state.subColumns));
      parts.push(buildMysqlFk(s, state.fkColumn, m, state.fkRefColumn));
    }
  } else {
    parts.push(buildPostgresTable(m, state.mainComment || m, state.mainColumns));
    parts.push(buildPostgresColumnComments(m, state.mainColumns));
    if (state.subEnabled && state.subTableName.trim()) {
      const s = state.subTableName.trim();
      parts.push(buildPostgresTable(s, state.subComment || s, state.subColumns));
      parts.push(buildPostgresColumnComments(s, state.subColumns));
      parts.push(buildPostgresFk(s, state.fkColumn, m, state.fkRefColumn));
    }
  }

  return parts.filter(Boolean).join("\n\n");
}
