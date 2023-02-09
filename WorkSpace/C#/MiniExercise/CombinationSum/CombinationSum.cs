public class Solution
{
    void backtrack(int[] candidatess, int target, IList<int> tmp, IList<IList<int>> result, int start)
    {
        if (target < 0) return;
        if (target == 0) result.Add(new List<int>(tmp));
        for (int i = start; i < candidatess.Length; i++)
        {
            tmp.Add(candidatess[i]);
            backtrack(candidatess, target - candidatess[i], tmp, result, i);
            tmp.RemoveAt(tmp.Count - 1);
        }
    }

    public IList<IList<int>> CombinationSum(int[] candidates, int target)
    {
        IList<IList<int>> result = new List<IList<int>>();
        IList<int> tmp = new List<int>();


        backtrack(candidates, target, tmp, result, 0);

        return result;
    }
}

