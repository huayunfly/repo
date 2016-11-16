//
//  PIDTune.cpp
//  Arduino_Libs
//
//  Created by huayun on 2016/11/7.
//  Classic PID algorithm is used.
//
//

#include <math.h>
#include "PIDTune.h"

double PIDTune::tune()
{
    ek_2 = ek_1;
    ek_1 = ek;
    ek = target - current;
    
    // Max or minimum ouput
    if (fabs(ek) > tuneRange)
    {
        if (isPosFeedback && ek > 0.0)
        {
            lastTuneVal = lowLimit;
        }
        else if (isPosFeedback && ek < 0.0)
        {
            lastTuneVal = highLimit;
        }
        else if (!isPosFeedback && ek > 0.0)
        {
            lastTuneVal = highLimit;
        }
        else if (!isPosFeedback && ek < 0.0)
        {
            lastTuneVal = lowLimit;
        }
    }
    else if (fabs(ek) < deadBand)
    {
        ; // we do nothing
    }
    else
    {
        float inc = ek * (interval / 1000.) / ti + (ek - ek_1);
        inc += td / (interval / 1000.) * (ek + ek_2 - 2 * ek_1);
        inc *= 1 / kp;
        // Limit the increment
        if (inc > maxInc)
        {
            inc = maxInc;
        }
        else if (inc < -maxInc)
        {
            inc = -maxInc;
        }
        if (isPosFeedback)
        {
            lastTuneVal -= inc;
        }
        else
        {
            lastTuneVal += inc;
        }
    }
    
    // Output limit
    if (lastTuneVal > highLimit)
    {
        lastTuneVal = highLimit;
    }
    else if (lastTuneVal < lowLimit)
    {
        lastTuneVal = lowLimit;
    }
    return lastTuneVal;
}


