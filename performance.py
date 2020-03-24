import numpy as np 
import pandas as pd 

def create_sharpe_ratio(returns,periods=252):
    #기본 일별수익률을 연간샤프레이쇼로 변환 period=252(일)*6.5(시)*60(분)
    return np.sqrt(periods)*(np.mean(returns))/np.std(returns)
def create_drawdowns(pnl):
    hwm=[0]
    idx=pnl.index
    drawdown=pd.Series(index=idx)
    duration=pd.Series(index=idx)
    for t in range(1,len(idx)):
        hwm.append(max(hwm[t-1],pnl[t])) # making high water mark
        drawdown[t]=(hwm[t]-pnl[t])
        duration[t]=(0 if drawdown[t] == 0 else duration[t-1]+1)
        return drawdown,drawdown.max(),duration.max()
        