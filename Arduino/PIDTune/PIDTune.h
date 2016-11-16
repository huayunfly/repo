//
//  PIDTune.hpp
//  Arduino_Libs
//
//  Created by huayun on 2016/11/7.
//
//

#ifndef PIDTune_hpp
#define PIDTune_hpp

class PIDTune
{
public:
    PIDTune()
    {
        target = 0.0;
        current = 0.0;
        lastTuneVal = 0.0;
        tuneRange = 80.0;
        ek = 0.0;
        ek_1 = 0.0;
        ek_2 = 0.0;
        interval = 2000;
        highLimit = 0.95;
        lowLimit = 0.0;
        kp = 200.0;
        ti = 1000.0;
        td = 0.0;
        deadBand = 0.1;
        maxInc = 0.5 * (highLimit - lowLimit);
        isPosFeedback = false;
        isKeepRunning = true;
    }
    ~PIDTune()
    {
        ;
    }
    
public:
    // PID algorithm's main routine
    double tune();
    
    // Get groups
    double output()
    {
        return lastTuneVal;
    }
    
    // Set groups
    void setTarget(double val)
    {
        target = val;
    }
    void setCurrent(double val)
    {
        current = val;
    }
    void setTuneRange(double val)
    {
        tuneRange = val;
    }
    void setInterval(double val)
    {
        interval = val;
    }
    void setHighLimit(double val)
    {
        highLimit = val;
    }
    void setLowLimit(double val)
    {
        lowLimit = val;
    }
    void setKp(double val)
    {
        kp = val;
    }
    void setTi(double val)
    {
        ti = val;
    }
    void setTd(double val)
    {
        td = val;
    }
    void setDeadband(double val)
    {
        deadBand = val;
    }
    void setMaxInc(double val)
    {
        maxInc = val;
    }
    void setPositiveFeedback(bool positive)
    {
        isPosFeedback = positive;
    }
    void setRunning(bool running)
    {
        isKeepRunning = running;
    }

    
private:
    PIDTune(const PIDTune&);
    PIDTune& operator=(const PIDTune&);
    
private:
    // PID parameter group
    double target;
    double current;
    double lastTuneVal;  // last tuning value
    double tuneRange;  // PID tuning range, compare with abs(ek)
    double ek; // e(k)
    double ek_1; // e(k-1)
    double ek_2; // e(k-2)
    unsigned long interval; // in ms, it will be transferred to second used by PID T
    double highLimit;  // PID output high limit
    double lowLimit; // PID output low limit
    double kp; // PID Kp
    double ti; // PID Ti
    double td; // PID Td
    double deadBand; // PID dead band: compare with abs(ek), units like celsius degree
    double maxInc; // maximum output increment
    bool isPosFeedback; // PID positive feedback
    bool isKeepRunning;
    
};

#endif /* PIDTune_hpp */

