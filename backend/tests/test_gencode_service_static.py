"""代码生成器服务静态规则覆盖。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.exceptions import CustomException
from app.modules.generator.gencode.schema import GenTableColumnSchema, GenTableOutSchema, GenTableSchema
from app.modules.generator.gencode.service import GenTableService


def test_route_and_catalog_keys() -> None:
    assert GenTableService._menu_route_first_segment(None, "system", None) == "module_system"
    assert GenTableService._menu_route_first_segment(None, "module_system", None) == "module_system"
    svc = GenTableService.__new__(GenTableService)
    assert svc._catalog_menu_dir_key(None, "module_system", "user") == "user"
    with pytest.raises(CustomException):
        svc._catalog_menu_dir_key(None, "", "user")
    with pytest.raises(CustomException):
        svc._catalog_menu_dir_key(None, "module_system", "")


def test_master_sub_rules() -> None:
    GenTableService.normalize_and_validate_master_sub(GenTableSchema(table_name="m"))
    with pytest.raises(CustomException, match="同时填写"):
        GenTableService.normalize_and_validate_master_sub(GenTableSchema(table_name="m", sub_table_name="s"))
    with pytest.raises(CustomException, match="不能与主表"):
        GenTableService.normalize_and_validate_master_sub(GenTableSchema(table_name="m", sub_table_name="m", sub_table_fk_name="m_id"))


def test_assert_master_sub_config() -> None:
    GenTableService._assert_master_sub_config_valid(GenTableOutSchema(table_name="m"))
    with pytest.raises(CustomException, match="同时填写"):
        GenTableService._assert_master_sub_config_valid(GenTableOutSchema(table_name="m", sub_table_name="s"))
    with pytest.raises(CustomException, match="无法生成"):
        GenTableService._assert_master_sub_config_valid(GenTableOutSchema(table_name="m", sub_table_name="s", sub_table_fk_name="m_id"))


async def test_set_pk_column() -> None:
    svc = GenTableService.__new__(GenTableService)
    t = GenTableOutSchema(table_name="m", columns=[GenTableColumnSchema(column_name="id"), GenTableColumnSchema(column_name="name")])
    await svc.set_pk_column(t)
    assert t.pk_column.column_name == "id"
    t2 = GenTableOutSchema(table_name="m", columns=[])
    await svc.set_pk_column(t2)
    assert t2.pk_column is None


async def test_preview_code_missing_and_render(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.generator.gencode import service as svc_mod
    from app.modules.generator.gencode.schema import GenTableOutSchema
    class CRUD:
        def __init__(self,*a): pass
        async def get_gen_table_by_id(self, id, preload=None): return None
    monkeypatch.setattr(svc_mod, "GenTableCRUD", CRUD)
    svc = GenTableService.__new__(GenTableService); svc.auth = object(); svc.db = object()
    with pytest.raises(CustomException, match="业务表不存在"):
        await svc.preview_code(1)

    table = GenTableOutSchema(table_name="demo", package_name="module_demo")
    class CRUD2:
        def __init__(self,*a): pass
        async def get_gen_table_by_id(self, id, preload=None): return table
    monkeypatch.setattr(svc_mod, "GenTableCRUD", CRUD2)
    async def set_pk(t): pass
    async def hydrate(t): pass
    async def pkg(*a): return "module_demo"
    svc.set_pk_column = set_pk; svc.hydrate_sub_table = hydrate; svc._effective_package_name = pkg
    class Tpl:
        async def render_async(self, **ctx): return "code"
    class Env:
        def get_template(self, name): return Tpl()
    class J:
        @staticmethod
        def get_env(): return Env()
        @staticmethod
        def prepare_context(t): return {}
        @staticmethod
        def get_template_list(): return ["a.py"]
        @staticmethod
        def get_file_name(t, g): return "a.py"
    monkeypatch.setattr(svc_mod, "Jinja2TemplateUtil", J)
    out = await svc.preview_code(1)
    assert out == {"a.py": "code"}


async def test_gen_table_queries(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableColumnOutSchema, GenTableOutSchema, GenTableQueryParam
    table = GenTableOutSchema(id=1, table_name="demo")
    class C:
        def __init__(self, *a): pass
        async def page(self, **kw): return SimpleNamespace(items=[table], total=1)
        async def get_db_table_page(self, **kw): return ([{"table_name": "demo"}], 1)
        async def get_db_table_list_by_names(self, names): return [SimpleNamespace(model_dump=lambda: {"table_name": "demo"})]
        async def get_gen_db_table_columns_by_name(self, name): return [{"column_name": "id", "column_type": "int"}]
    monkeypatch.setattr(mod, "GenTableCRUD", C)
    monkeypatch.setattr(mod, "GenTableColumnCRUD", C)
    s = GenTableService.__new__(GenTableService); s.auth = object(); s.db = object()
    async def by_id(i): return table
    s.get_gen_table_by_id = by_id
    assert (await s.get_gen_table_detail(1)).table_name == "demo"
    page = await s.get_gen_table_page(1, 10, GenTableQueryParam())
    assert page.total == 1 and page.items[0].table_name == "demo"
    db_page = await s.get_gen_db_table_page(1, 10, GenTableQueryParam())
    assert db_page["total"] == 1
    assert (await s.get_gen_db_table_list_by_name(["demo"]))[0].table_name == "demo"
    cols = await s._get_db_table_columns("demo")
    assert cols[0].column_name == "id"


async def test_import_gen_table(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableColumnOutSchema, GenTableOutSchema
    class C:
        def __init__(self, *a): pass
        async def get_gen_table_by_name(self, name): return None
        async def add_gen_table(self, data): return SimpleNamespace(id=9)
        async def create_gen_table_column_crud(self, col): return col
    monkeypatch.setattr(mod, "GenTableCRUD", C)
    monkeypatch.setattr(mod, "GenTableColumnCRUD", C)
    s = GenTableService.__new__(GenTableService); s.auth = object(); s.db = object()
    async def cols(name): return [GenTableColumnOutSchema(column_name="id", column_type="int", column_length="")]
    s._get_db_table_columns = cols
    table = GenTableOutSchema(table_name="demo", table_comment="Demo")
    assert await s.import_gen_table([table]) is True
    with pytest.raises(CustomException, match="不能为空"):
        await s.import_gen_table([])
    class C2(C):
        async def get_gen_table_by_name(self, name): return object()
    monkeypatch.setattr(mod, "GenTableCRUD", C2)
    with pytest.raises(CustomException, match="已存在"):
        await s.import_gen_table([GenTableOutSchema(table_name="demo")])


async def test_get_gen_table_by_id(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableOutSchema
    class C:
        def __init__(self, *a): pass
        async def get_gen_table_by_id(self, id, preload=None): return None
    monkeypatch.setattr(mod, "GenTableCRUD", C)
    s = GenTableService.__new__(GenTableService); s.auth = object(); s.db = object()
    with pytest.raises(CustomException, match="不存在"):
        await s.get_gen_table_by_id(1)
    class C2(C):
        async def get_gen_table_by_id(self, id, preload=None): return GenTableOutSchema(id=1, table_name="demo")
    monkeypatch.setattr(mod, "GenTableCRUD", C2)
    async def pk(t): return None
    async def sub(t): return None
    s.set_pk_column = pk; s.hydrate_sub_table = sub
    assert (await s.get_gen_table_by_id(1)).table_name == "demo"


async def test_write_plugin_migration(monkeypatch: pytest.MonkeyPatch) -> None:
    import alembic.command as cmd
    import alembic.config as cfg
    import alembic.script as script
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableOutSchema
    calls=[]
    class C:
        def __init__(self, *a): pass
    class S:
        def __init__(self, *a): pass
        def get_heads(self): return ["h"]
    monkeypatch.setattr(cfg, "Config", C)
    monkeypatch.setattr(script, "ScriptDirectory", type("SD", (), {"from_config": staticmethod(lambda c: S())}))
    monkeypatch.setattr(cmd, "revision", lambda *a, **k: calls.append(k))
    s = GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    await s._write_plugin_migration(GenTableOutSchema(table_name="demo"))
    assert calls


async def test_write_plugin_migration_multiple_heads(monkeypatch: pytest.MonkeyPatch) -> None:
    import alembic.command as cmd, alembic.config as cfg, alembic.script as script
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableOutSchema
    class C:
        def __init__(self,*a): pass
    class S:
        def get_heads(self): return ["a","b"]
    monkeypatch.setattr(cfg,"Config",C)
    monkeypatch.setattr(script,"ScriptDirectory",type("SD",(),{"from_config":staticmethod(lambda c:S())}))
    monkeypatch.setattr(cmd,"revision",lambda *a,**k: None)
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    with pytest.raises(CustomException, match="多个 head"):
        await s._write_plugin_migration(GenTableOutSchema(table_name="demo"))


async def test_package_directory_menu(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    class M:
        def __init__(self,*a): self.created=[]
        async def get(self,**kw): return None
        async def create(self,data): self.created.append(data); return SimpleNamespace(id=9)
    m=M(); s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    assert await s._get_or_create_package_directory_menu(m,None,"module_demo","demo","demo") == 9
    class M2(M):
        async def get(self,**kw): return SimpleNamespace(id=8)
    assert await s._get_or_create_package_directory_menu(M2(),None,"module_demo","demo","demo") == 8


async def test_assert_parent_catalog(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    import app.modules.generator.gencode.service as mod
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    await s._assert_parent_menu_is_catalog(None)
    class M:
        def __init__(self,*a): pass
        async def get(self,**kw): return None
    monkeypatch.setattr(mod,"MenuCRUD",M)
    with pytest.raises(CustomException, match="不存在"):
        await s._assert_parent_menu_is_catalog(1)
    class M2(M):
        async def get(self,**kw): return SimpleNamespace(type=2)
    monkeypatch.setattr(mod,"MenuCRUD",M2)
    with pytest.raises(CustomException, match="目录"):
        await s._assert_parent_menu_is_catalog(1)
    class M3(M2):
        async def get(self,**kw): return SimpleNamespace(type=1)
    monkeypatch.setattr(mod,"MenuCRUD",M3)
    await s._assert_parent_menu_is_catalog(1)


async def test_effective_package_name(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace
    import app.modules.generator.gencode.service as mod
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    assert await s._effective_package_name(None,"demo") == "module_demo"
    assert await s._effective_package_name(None,"module_demo") == "module_demo"
    with pytest.raises(CustomException, match="包名不能为空"):
        await s._effective_package_name(None,"")
    class M:
        def __init__(self,*a): pass
        async def get(self,**kw): return SimpleNamespace(route_path="/module_sys/demo")
    monkeypatch.setattr(mod,"MenuCRUD",M)
    assert await s._effective_package_name(1,"x") == "module_sys"
    class M2(M):
        async def get(self,**kw): return SimpleNamespace(route_path="")
    monkeypatch.setattr(mod,"MenuCRUD",M2)
    assert await s._effective_package_name(1,"demo") == "module_demo"
    with pytest.raises(CustomException, match="无法从上级"):
        await s._effective_package_name(1,"")


async def test_package_directory_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    class M:
        def __init__(self,*a): pass
    with pytest.raises(CustomException, match="包名不能为空"):
        await s._get_or_create_package_directory_menu(M(),None,"","demo","demo")
    with pytest.raises(CustomException, match="模块名不能为空"):
        await s._get_or_create_package_directory_menu(M(),None,"module_demo","","demo")


async def test_package_directory_existing_with_parent() -> None:
    from types import SimpleNamespace
    class M:
        def __init__(self,*a): pass
        async def get(self,**kw): return SimpleNamespace(id=7)
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    assert await s._get_or_create_package_directory_menu(M(),1,"module_demo","demo","demo") == 7


async def test_delete_gen_table(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    class C:
        def __init__(self,*a): pass
        async def delete_gen_table_column_by_table_id_crud(self, ids): self.cols=ids
        async def delete_gen_table(self, ids): self.tables=ids
    monkeypatch.setattr(mod,"GenTableCRUD",C); monkeypatch.setattr(mod,"GenTableColumnCRUD",C)
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    with pytest.raises(CustomException, match="不能为空"):
        await s.delete_gen_table([])
    await s.delete_gen_table([1])


async def test_delete_gen_table_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    class C:
        def __init__(self,*a): pass
        async def delete_gen_table_column_by_table_id_crud(self, ids): raise RuntimeError()
    monkeypatch.setattr(mod,"GenTableColumnCRUD",C)
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    with pytest.raises(RuntimeError):
        await s.delete_gen_table([1])


async def test_write_plugin_migration_no_heads(monkeypatch: pytest.MonkeyPatch) -> None:
    import alembic.command as cmd, alembic.config as cfg, alembic.script as script
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableOutSchema
    calls=[]
    class C:
        def __init__(self,*a): pass
    class S:
        def get_heads(self): return []
    monkeypatch.setattr(cfg,"Config",C)
    monkeypatch.setattr(script,"ScriptDirectory",type("SD",(),{"from_config":staticmethod(lambda c:S())}))
    monkeypatch.setattr(cmd,"revision",lambda *a,**kw: calls.append(kw))
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    await s._write_plugin_migration(GenTableOutSchema(table_name="demo"))
    assert calls and calls[0]["head"] is None


async def test_update_gen_table_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableOutSchema, GenTableSchema
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    async def none_id(i): return GenTableOutSchema(table_name="d")
    s.get_gen_table_by_id=none_id
    with pytest.raises(CustomException, match="不存在"):
        await s.update_gen_table(GenTableSchema(table_name="d"),1)
    async def one(i): return GenTableOutSchema(id=1,table_name="d")
    s.get_gen_table_by_id=one
    class C:
        def __init__(self,*a): pass
        async def edit_gen_table(self,*a): return None
    monkeypatch.setattr(mod,"GenTableCRUD",C)
    with pytest.raises(CustomException, match="更新业务表信息失败"):
        await s.update_gen_table(GenTableSchema(table_name="d"),1)
    class C2(C):
        async def edit_gen_table(self,*a): return True
        async def get_gen_table_by_id(self,*a,**k): return {"id":1,"table_name":"d"}
    monkeypatch.setattr(mod,"GenTableCRUD",C2)
    async def noop(*a,**k): return None
    s._assert_parent_menu_is_catalog=noop; s.set_pk_column=noop; s.hydrate_sub_table=noop
    out=await s.update_gen_table(GenTableSchema(table_name="d"),1)
    assert out.table_name=="d"


async def test_update_gen_table_columns(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableColumnOutSchema, GenTableOutSchema, GenTableSchema
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    async def one(i): return GenTableOutSchema(id=1,table_name="d")
    s.get_gen_table_by_id=one
    class T:
        def __init__(self,*a): pass
        async def edit_gen_table(self,*a): return True
        async def get_gen_table_by_id(self,*a,**k): return {"id":1,"table_name":"d"}
    class C:
        def __init__(self,*a): self.calls=[]
        async def list_gen_table_column_crud(self,**k): return [SimpleNamespace(id=1,column_name="a"),SimpleNamespace(id=2,column_name="gone")]
        async def update(self,**k): self.calls.append(("update",k))
        async def create_gen_table_column_crud(self,data): self.calls.append(("create",data))
        async def delete(self,**k): self.calls.append(("delete",k))
    c=C(); monkeypatch.setattr(mod,"GenTableCRUD",T); monkeypatch.setattr(mod,"GenTableColumnCRUD",lambda *a:c)
    async def noop(*a,**k): return None
    s._assert_parent_menu_is_catalog=noop; s.set_pk_column=noop; s.hydrate_sub_table=noop
    old=GenTableColumnOutSchema(id=1,column_name="a",column_type="int")
    new=GenTableColumnOutSchema(column_name="b",column_type="int")
    data=GenTableSchema(table_name="d",columns=[old,new])
    out=await s.update_gen_table(data,1)
    assert out.table_name=="d"
    assert any(x[0]=="update" for x in c.calls) and any(x[0]=="create" for x in c.calls) and any(x[0]=="delete" for x in c.calls)


async def test_sync_db_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableOutSchema
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    with pytest.raises(CustomException, match="表名不能为空"):
        await s.sync_db("")
    class C:
        def __init__(self,*a): self.obj=None
        async def get_gen_table_by_name(self,*a,**k): return self.obj
    c=C(); monkeypatch.setattr(mod,"GenTableCRUD",lambda *a:c)
    with pytest.raises(CustomException, match="业务表不存在"):
        await s.sync_db("d")
    c.obj=GenTableOutSchema(table_name="d")
    with pytest.raises(CustomException, match="业务表ID不能为空"):
        await s.sync_db("d")
    c.obj=GenTableOutSchema(id=1,table_name="d")
    async def cols(name): return []
    s._get_db_table_columns=cols
    await s.sync_db("d")


async def test_sync_db_columns(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableColumnOutSchema, GenTableOutSchema
    table=GenTableOutSchema(id=1,table_name="d",columns=[GenTableColumnOutSchema(id=1,column_name="a")])
    db_cols=[GenTableColumnOutSchema(column_name="a"),GenTableColumnOutSchema(column_name="b")]
    class C:
        def __init__(self,*a): self.obj=table
        async def get_gen_table_by_name(self,*a,**k): return self.obj
    c=C(); monkeypatch.setattr(mod,"GenTableCRUD",lambda *a:c)
    calls=[]
    class Col:
        def __init__(self,*a): pass
        async def update_gen_table_column_crud(self,i,d): calls.append(("update",i))
        async def create_gen_table_column_crud(self,d): calls.append(("create",d.column_name))
        async def delete_gen_table_column_by_column_id_crud(self,ids): calls.append(("delete",ids))
    monkeypatch.setattr(mod,"GenTableColumnCRUD",Col)
    monkeypatch.setattr(mod.GenUtils,"init_column_field",staticmethod(lambda col,t:None))
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    async def cols(name): return db_cols
    s._get_db_table_columns=cols
    await s.sync_db("d")
    assert any(x[0]=="update" for x in calls) and any(x[0]=="create" and x[1]=="b" for x in calls)


async def test_sync_db_delete_and_error(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableColumnOutSchema, GenTableOutSchema
    table=GenTableOutSchema(id=1,table_name="d",columns=[GenTableColumnOutSchema(id=2,column_name="gone")])
    class C:
        def __init__(self,*a): self.obj=table
        async def get_gen_table_by_name(self,*a,**k): return self.obj
    monkeypatch.setattr(mod,"GenTableCRUD",lambda *a:C())
    calls=[]
    class Col:
        def __init__(self,*a): pass
        async def delete_gen_table_column_by_column_id_crud(self,ids): calls.append(ids)
    monkeypatch.setattr(mod,"GenTableColumnCRUD",Col)
    monkeypatch.setattr(mod.GenUtils,"init_column_field",staticmethod(lambda col,t:None))
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    async def cols(name): return []
    s._get_db_table_columns=cols
    await s.sync_db("d")
    assert calls == [[2]]
    def bad(*a): raise RuntimeError()
    monkeypatch.setattr(mod.GenUtils,"init_column_field",staticmethod(bad))
    s._get_db_table_columns=lambda name: _async([GenTableColumnOutSchema(column_name="x")])
    with pytest.raises(RuntimeError):
        await s.sync_db("d")


async def _async(v): return v


async def test_sync_db_preserve_and_sub(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.generator.gencode.service as mod
    from app.modules.generator.gencode.schema import GenTableColumnOutSchema, GenTableOutSchema
    prev=GenTableColumnOutSchema(id=1,column_name="a",is_pk=True,is_insert=True,is_edit=True,is_list=True,is_query=True,html_type="input",dict_type="d",sort=2)
    table=GenTableOutSchema(id=1,table_name="d",columns=[prev],sub_table_name="sub",sub_table_fk_name="fk")
    db=GenTableColumnOutSchema(column_name="a",is_pk=True)
    class C:
        def __init__(self,*a): self.n=0
        async def get_gen_table_by_name(self,name,*a,**k):
            if name=="sub": return GenTableOutSchema(id=2,table_name="sub")
            return table
    monkeypatch.setattr(mod,"GenTableCRUD",lambda *a:C())
    updated=[]
    class Col:
        def __init__(self,*a): pass
        async def update_gen_table_column_crud(self,i,d): updated.append(d)
    monkeypatch.setattr(mod,"GenTableColumnCRUD",Col)
    monkeypatch.setattr(mod.GenUtils,"init_column_field",staticmethod(lambda c,t:None))
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    async def cols(name): return [db] if name=="d" else []
    s._get_db_table_columns=cols
    await s.sync_db("d")
    d=updated[0]
    assert d.is_insert is False and d.dict_type=="d" and d.sort==2


async def test_write_plugin_migration_success(monkeypatch: pytest.MonkeyPatch) -> None:
    import alembic.command as cmd, alembic.config as cfg, alembic.script as script
    from app.modules.generator.gencode.schema import GenTableOutSchema
    calls=[]
    class C:
        def __init__(self,*a): pass
    class S:
        def get_heads(self): return ["h"]
    monkeypatch.setattr(cfg,"Config",C)
    monkeypatch.setattr(script,"ScriptDirectory",type("SD",(),{"from_config":staticmethod(lambda c:S())}))
    monkeypatch.setattr(cmd,"revision",lambda *a,**k: calls.append(k))
    s=GenTableService.__new__(GenTableService); s.auth=object(); s.db=object()
    await s._write_plugin_migration(GenTableOutSchema(table_name="demo"))
    assert calls and calls[0]["head"]=="h"
