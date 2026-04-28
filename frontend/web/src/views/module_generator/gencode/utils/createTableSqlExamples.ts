import { buildSqlFromVisual } from './buildCreateTableSql';
import {
  applySubColumns,
  visualPresetMasterSub,
  visualPresetSingle,
} from './createTableVisualPresets';

/** 与「表结构」单表模板一致的 SQL（便于两种模式对齐） */
export function getExampleFromPresetSingle(dialect: 'mysql' | 'postgres'): string {
  return buildSqlFromVisual(visualPresetSingle(dialect));
}

/** 与「表结构」主子表模板一致的 SQL */
export function getExampleFromPresetMasterSub(dialect: 'mysql' | 'postgres'): string {
  return buildSqlFromVisual(applySubColumns(visualPresetMasterSub(dialect)));
}
