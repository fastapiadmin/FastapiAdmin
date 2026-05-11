/**
 * 通用文件下载（axios + blob），非 Vue 插件。
 */
import axios from "axios";
import { ElLoading, ElMessage } from "element-plus";
import { saveAs as fileSaverSaveAs } from "file-saver";
import { Auth } from "@utils/auth";
import { errorCode } from "@utils/constants";
import { blobValidate } from "@utils/common";

const baseURL = import.meta.env.VITE_APP_BASE_API;
let downloadLoadingInstance: any;

interface DownloadUtil {
  name(name: string, isDelete?: boolean): void;
  resource(resource: string): void;
  zip(url: string, name: string): void;
  saveAs(text: Blob | string, name: string, opts?: any): void;
  printErrMsg(data: Blob): Promise<void>;
}

const download: DownloadUtil = {
  async name(name: string, isDelete: boolean = true) {
    const url =
      baseURL + "/common/download?fileName=" + encodeURIComponent(name) + "&delete=" + isDelete;
    try {
      const res = await axios.get<Blob>(url, {
        responseType: "blob",
        headers: { Authorization: `Bearer ${Auth.getAccessToken()}` },
      });
      const isBlob = blobValidate(res.data);
      if (isBlob) {
        const blob = new Blob([res.data]);
        download.saveAs(blob, decodeURIComponent(res.headers["download-filename"]));
      } else {
        await download.printErrMsg(res.data);
      }
    } catch (error) {
      console.error("[Download] 文件下载失败:", error);
      ElMessage.error("下载文件失败，请稍后重试");
    }
  },

  async resource(resource: string) {
    const url = baseURL + "/common/download/resource?resource=" + encodeURIComponent(resource);
    try {
      const res = await axios.get<Blob>(url, {
        responseType: "blob",
        headers: { Authorization: `Bearer ${Auth.getAccessToken()}` },
      });
      const isBlob = blobValidate(res.data);
      if (isBlob) {
        const blob = new Blob([res.data]);
        download.saveAs(blob, decodeURIComponent(res.headers["download-filename"]));
      } else {
        await download.printErrMsg(res.data);
      }
    } catch (error) {
      console.error("[Download] 资源下载失败:", error);
      ElMessage.error("资源下载失败，请稍后重试");
    }
  },

  async zip(url: string, name: string) {
    const fullUrl = baseURL + url;
    downloadLoadingInstance = ElLoading.service({
      text: "正在下载数据，请稍候",
      background: "rgba(0, 0, 0, 0.7)",
    });
    try {
      const res = await axios.get<Blob>(fullUrl, {
        responseType: "blob",
        headers: { Authorization: `Bearer ${Auth.getAccessToken()}` },
      });
      const isBlob = blobValidate(res.data);
      if (isBlob) {
        const blob = new Blob([res.data], { type: "application/zip" });
        download.saveAs(blob, name);
      } else {
        await download.printErrMsg(res.data);
      }
    } catch (r: any) {
      console.error(r);
      ElMessage.error("下载文件出现错误，请联系管理员！");
    } finally {
      downloadLoadingInstance.close();
    }
  },

  saveAs(text: Blob | string, name: string, opts?: any): void {
    fileSaverSaveAs(text, name, opts);
  },

  async printErrMsg(data: Blob): Promise<void> {
    const resText = await data.text();
    const rspObj = JSON.parse(resText);
    const errMsg = errorCode[rspObj.code] || rspObj.msg || errorCode["default"];
    ElMessage.error(errMsg);
  },
};

export default download;
