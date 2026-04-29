import axios, { AxiosResponse } from "axios";
import { ElLoading, ElMessage } from "element-plus";
import { saveAs as fileSaverSaveAs } from "file-saver";
import { Auth } from "@/utils/auth";
import errorCode from "@/utils/errorCode";
import { blobValidate } from "@/utils/common";

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
  name(name: string, isDelete: boolean = true): void {
    const url =
      baseURL + "/common/download?fileName=" + encodeURIComponent(name) + "&delete=" + isDelete;
    axios({
      method: "get",
      url,
      responseType: "blob",
      headers: { Authorization: "Bearer " + Auth.getAccessToken() },
    }).then((res: AxiosResponse<Blob>) => {
      const isBlob = blobValidate(res.data);
      if (isBlob) {
        const blob = new Blob([res.data]);
        download.saveAs(blob, decodeURIComponent(res.headers["download-filename"]));
      } else {
        download.printErrMsg(res.data);
      }
    });
  },

  resource(resource: string): void {
    const url = baseURL + "/common/download/resource?resource=" + encodeURIComponent(resource);
    axios({
      method: "get",
      url,
      responseType: "blob",
      headers: { Authorization: "Bearer " + Auth.getAccessToken() },
    }).then((res: AxiosResponse<Blob>) => {
      const isBlob = blobValidate(res.data);
      if (isBlob) {
        const blob = new Blob([res.data]);
        download.saveAs(blob, decodeURIComponent(res.headers["download-filename"]));
      } else {
        download.printErrMsg(res.data);
      }
    });
  },

  zip(url: string, name: string): void {
    const fullUrl = baseURL + url;
    downloadLoadingInstance = ElLoading.service({
      text: "正在下载数据，请稍候",
      background: "rgba(0, 0, 0, 0.7)",
    });
    axios({
      method: "get",
      url: fullUrl,
      responseType: "blob",
      headers: { Authorization: "Bearer " + Auth.getAccessToken() },
    })
      .then((res: AxiosResponse<Blob>) => {
        const isBlob = blobValidate(res.data);
        if (isBlob) {
          const blob = new Blob([res.data], { type: "application/zip" });
          download.saveAs(blob, name);
        } else {
          download.printErrMsg(res.data);
        }
        downloadLoadingInstance.close();
      })
      .catch((r: any) => {
        console.error(r);
        ElMessage.error("下载文件出现错误，请联系管理员！");
        downloadLoadingInstance.close();
      });
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
