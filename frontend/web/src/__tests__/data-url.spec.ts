import { describe, expect, it } from "vitest";
import { dataURLToFile } from "@/utils/file/dataUrl";

describe("dataURLToFile", () => {
  it("无效 data URL 抛错", () => expect(() => dataURLToFile("bad", "a")).toThrow("Invalid data URL"));
  it("解析 mime 与文件名", async () => {
    const f = dataURLToFile("data:image/jpeg;base64,QQ==", "a.jpg");
    expect(f.name).toBe("a.jpg");
    expect(f.type).toBe("image/jpeg");
    expect(await f.text()).toBe("A");
  });
  it("无 mime 时回退 image/png", () => {
    expect(dataURLToFile("data:;base64,QQ==", "a").type).toBe("image/png");
  });
  it("保留二进制内容", async () => {
    const f = dataURLToFile("data:image/png;base64,AAEC", "a.png");
    expect(new Uint8Array(await f.arrayBuffer())).toEqual(new Uint8Array([0, 1, 2]));
  });
});
