namespace Курсач;

public class Product
{
    public string name;
    public float assessedValue, outpostSum;
    public DateTime wasDelivered, savingsTerm;

    public Product(string name, float assessedValue, float outpostSum, int savingDays)
    {
        this.name = name;
        this.assessedValue = assessedValue;
        this.outpostSum = outpostSum;
        wasDelivered = DateTime.Now;
        savingsTerm = wasDelivered.AddDays(savingDays);
    }
}