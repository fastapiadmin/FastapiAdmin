/**
 * 将 Data URL（base64）转为 {@link File}，便于上传裁剪结果。
 */
export function dataURLToFile(dataURL: string, filename: string): File {
  const comma = dataURL.indexOf(",");
  if (comma === -1) {
    throw new Error("Invalid data URL");
  }
  const header = dataURL.slice(0, comma);
  const base64 = dataURL.slice(comma + 1);
  const mimeMatch = header.match(/data:(.*?);/);
  const mime = mimeMatch?.[1] ?? "image/png";

  const binary = atob(base64);
  const len = binary.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return new File([bytes], filename, { type: mime });
}
