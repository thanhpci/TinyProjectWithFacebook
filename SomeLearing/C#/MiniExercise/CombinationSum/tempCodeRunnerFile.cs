IList> result = new IList<>();

        IList<int> tmp = new IList<int>();

        backtrack(candidates, target, tmp, result, 0);

        return result;