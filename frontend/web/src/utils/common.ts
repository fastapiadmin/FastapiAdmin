// 问候语：根据当前小时返回不同问候语
export function greetings() {
  // 当前时间（用于计算问候语）
  const currentDate = new Date();
  const hours = currentDate.getHours();
  if (hours >= 6 && hours < 8) {
    return '晨起披衣出草堂，轩窗已自喜微凉🌅！';
  } else if (hours >= 8 && hours < 12) {
    return `上午好！`;
  } else if (hours >= 12 && hours < 14) {
    return `中午好！`;
  } else if (hours >= 14 && hours < 18) {
    return `下午好！`;
  } else if (hours >= 18 && hours < 24) {
    return `晚上好！`;
  } else {
    return '偷偷向银河要了一把碎星，只等你闭上眼睛撒入你的梦中，晚安🌛！';
  }
}

export function getRangeDate(startDate: string | number | Date, endDate: string | number | Date) {
  const targetArr = [];
  const start = new Date(startDate);
  const end = new Date(endDate);
  const startDateInfo = {
    year: start.getFullYear(),
    month: start.getMonth() + 1,
    day: start.getDate(),
  };
  const endDateInfo = {
    year: end.getFullYear(),
    month: end.getMonth() + 1,
    day: end.getDate(),
  };
  if (startDateInfo.year === endDateInfo.year) {
    //同年
    if (startDateInfo.month !== endDateInfo.month) {
      //同年，不同月份
      //获取开始时间所在月的月底日期
      const startMax = new Date(startDateInfo.year, startDateInfo.month, 0).getDate();
      const endNum = startMax - startDateInfo.day + endDateInfo.day;
      for (let i = startDateInfo.day; i <= startDateInfo.day + endNum; i++) {
        if (i > startMax) {
          targetArr.push(
            `${endDateInfo.year}-${
              endDateInfo.month < 10 ? '0' + endDateInfo.month : endDateInfo.month
            }-${i - startMax < 10 ? '0' + (i - startMax) : i - startMax}`
          );
        } else {
          targetArr.push(
            `${startDateInfo.year}-${
              startDateInfo.month < 10 ? '0' + startDateInfo.month : startDateInfo.month
            }-${i < 10 ? '0' + i : i}`
          );
        }
      }
    } else {
      //同年同月
      for (let i = startDateInfo.day; i <= endDateInfo.day; i++) {
        targetArr.push(
          `${startDateInfo.year}-${
            startDateInfo.month < 10 ? '0' + startDateInfo.month : startDateInfo.month
          }-${i < 10 ? '0' + i : i}`
        );
      }
    }
  } else {
    //不同年   【既然不同年那肯定也不同月】
    const startMax = new Date(startDateInfo.year, startDateInfo.month, 0).getDate();
    const endNum = startMax - startDateInfo.day + endDateInfo.day;
    for (let i = startDateInfo.day; i <= startDateInfo.day + endNum; i++) {
      if (i > startMax) {
        targetArr.push(
          `${endDateInfo.year}-${
            endDateInfo.month < 10 ? '0' + endDateInfo.month : endDateInfo.month
          }-${i - startMax < 10 ? '0' + (i - startMax) : i - startMax}`
        );
      } else {
        targetArr.push(
          `${startDateInfo.year}-${
            startDateInfo.month < 10 ? '0' + startDateInfo.month : startDateInfo.month
          }-${i < 10 ? '0' + i : i}`
        );
      }
    }
  }

  return targetArr;
}

export function listToTree(list: any[]) {
  const map: { [key: string | number]: any } = {};
  // 创建映射表，保留每个节点的 parent_id 等原始字段
  list.forEach((item) => {
    map[item.id] = { ...item };
  });

  const tree: any[] = [];
  list.forEach((item) => {
    const parentId = item.parent_id;
    if (parentId && map[parentId]) {
      // 将当前节点加入其父节点的 children 数组中
      if (!map[parentId].children) {
        map[parentId].children = [];
      }
      map[parentId].children.push(map[item.id]);
    } else if (parentId === null || parentId === undefined) {
      // 根节点
      tree.push(map[item.id]);
    }
  });

  return tree;
}

// 加载部门选项
export function formatTree(nodes: any[]): any[] {
  return nodes.map((node) => {
    const formattedNode = {
      value: node.id,
      label: node.name,
      disabled: node.status === false || String(node.status) === 'false',
    };

    if (node.children && node.children.length > 0) {
      Object.assign(formattedNode, { children: formatTree(node.children) });
    }

    return formattedNode;
  });
}

export function cloneDeep(obj: any) {
  return JSON.parse(JSON.stringify(obj));
}

export function isEmpty(obj: string | null | undefined) {
  if (obj === undefined || obj === null || obj === '') {
    return true;
  } else {
    return false;
  }
}

// 验证是否为blob格式
export function blobValidate(data: Blob): boolean {
  return data.type !== 'application/json';
}
