# Episode 03B · Answers

1. Input IDs [0,1,3,1], target IDs [0,2,0,3]. Inputs include START; outputs include END.
2. Nine times ln(4) = 12.476649; divide by nine for 1.386294 nats/prediction.
3. Both stay the same within floating-point tolerance; the common exponential factor cancels.
4. No. The a row becomes [1/7,1/7,1/7,4/7]. Scaling changes probability ratios.
5. a→n and a→v worsen, while a→END improves. The other input rows do not change.
6. Correct full mean is (5*loss_anna + 4*loss_ava)/9. Equal name weighting generally differs.
7. An empty string with ended=True. START has a valid END output column.
8. The loop hit its safety limit; it never sampled END on that attempt.
9. exp(log(C+k)) normalized by row gives (C+k)/(row_total + k*number_of_outputs).
10. Add a derivative/gradient computation and an update rule applied to parameters.
    Current code only measures chosen settings; that training machinery is deferred.
