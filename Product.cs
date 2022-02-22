namespace Курсач;

public class Product
{
    public string name;

    public string Name
    {
        get => name;
        set => name = value ?? throw new ArgumentNullException(nameof(value));
    }

    public float AssessedValue
    {
        get => assessedValue;
        set => assessedValue = value;
    }

    public float OutpostSum
    {
        get => outpostSum;
        set => outpostSum = value;
    }

    public DateTime WasDelivered
    {
        get => wasDelivered;
        set => wasDelivered = value;
    }

    public DateTime SavingsTerm
    {
        get => savingsTerm;
        set => savingsTerm = value;
    }

    public float assessedValue;
    public float outpostSum;

    public DateTime wasDelivered;
    public DateTime savingsTerm;

    public Product(string name, float assessedValue, float outpostSum, int savingDays)
    {
        this.name = name;
        this.assessedValue = assessedValue;
        this.outpostSum = outpostSum;
        wasDelivered = DateTime.Now;
        savingsTerm = wasDelivered.AddDays(savingDays);
    }
}