class Work():
    def __init__(self, source_len_list, target_dict, cut=0, is_always_cut=False):
        # 原料列表（原始值）
        self.source_len_list = source_len_list
        self.source_len_list.sort(reverse=True)
        # 切割清单（原始值）
        self.target_dict = target_dict
        # 锯缝
        self.cut = cut
        # 最后一锯必留锯口
        self.is_always_cut = is_always_cut

        # 切割长度列表、切割数量列表
        self.target_len_list = list(target_dict.keys())
        self.target_num_list = list(target_dict.values())

        # 原料列表（程序计算值）
        self.cal_source_len_list = self.__cal_source()
        # 切割清单（程序计算值）
        self.cal_target_dict = self.__cal_target()

        # 每种原材料最多可以分割为多少单一目标,list[source_id][target_id]
        self.max_num = self.__cal_max_num()

        # 全部切割方案以及方案使用的原料（原始值）
        self.all_methods_list, self.all_methods_len_list = self.__get_all_methods()

    def get_methods_list_by_idxs(idx_list):
        return [self.all_methods_len_list[i] for i in idx_list]

    def get_method_dict_by_idx(idx):
        method = self.all_methods_list[idx]
        method_dict = {self.target_len_list[i]: method[i] for i in range(method)}
        return method_dict

    def get_methods_dict_list_by_idxs(idx_list):
        return [self.get_method_dict_by_idx(idx) for idx in idx_list]

    def get_methods_len_list_by_idx(idx_list):
        return [self]

    def __cal_max_num(self):
        max_list = []
        for source_len in self.cal_source_len_list:
            num_list = []
            for target_len, target_num in self.cal_target_dict.items():
                tmp_num = source_len // target_len
                mum_list.append(target_num if tmp_num >
                                target_num else tmp_num)
            max_list.append(num_list)
        return max_list

    def __cal_source(self):
        if not self.is_always_cut:
            cal_list = [source + self.cut for source in self.source_len_list]
            return cal_list
        return self.source_len_list[:]

    def __cal_target(self):
        if self.cut:
            cal_dict = {length+self.cut: num for length,
                        num in self.target_dict.items()}
            return cal_dict
        return self.target_dict.copy()

    def __get_all_methods(self):
        all_methods = []
        all_methods_len = []
        # 第一重循环：每种原料长度
        for source_idx, source_len in enumerate(self.cal_source_len_list):
            source_methods, source_methods_len = self.__get_methods(
                source_len, self.max_num[source_idx])
            all_methods += source_methods
            all_methods_len += source_methods_len
        return all_methods, all_methods_len

    def __get_methods(self, source_len, max_num_list):
        if not any(max_num_list):
            return []
        methods = []
        for i in range(max_num_list):
            if max_num_list(i):
                next_max_list = max_num_list[:]
                next_max_list[i] = 0
                for count in range(1,max_num_list[i] + 1)
        # methods = [[0] * len(self.cal_target_dict)]
        # methods_len = [0, ]
        # values = [0, ]
        # for idx, (length, max_count) in enumerate(self.cal_target_dict.items()):
        #     new_methods = []
        #     new_values = []
        #     new_methods_len = []
        #     for i, method in enumerate(methods):
        #         for count in range(max_count, 0, -1):
        #             is_break_two = False
        #             tmp_value = values[i] + length*count
        #             for source_idx, source_len in enumerate(self.cal_source_len_list):
        #                 if tmp_value <= source_len:
        #                     tmp_method = method[:]
        #                     tmp_method[idx] = count
        #                     new_methods.append(tmp_method)
        #                     new_values.append(tmp_value)
        #                     new_methods_len.append(source_len)
        #                     if source_idx == 0:
        #                         is_break_two = True
        #                     break
        #             if is_break_two:
        #                 break
        #     methods += new_methods
        #     methods_len += new_methods_len
        #     values += new_values
        # return methods, methods_len


if __name__ == "__main__":
    source_list = [6000, 3000]
    target_dict = {
        134: 48,
        400: 10,
        1900: 24
    }
    cut = 1
    w = Work(source_list, target_dict, cut)
    pass
