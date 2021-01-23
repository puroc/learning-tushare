basic = {
    'url': {
        'org_basic_info': 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=HSGTCOMSTA&token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDCOUNT&sr=3&p=${PAGE_NO}&ps=${PAGE_COUNT}&js=var%20LPMJumVs={pages:(tp),data:(x)}&filter=(MARKET=%${MARKET}%27)(HDDATE=^${DATE}^)&rt=53713175',
        'org_stock_info': 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDPRICE&sr=3&p=${PAGE_NO}&ps=${PAGE_COUNT}&js=var%20fRKiVjqQ={pages:(tp),data:(x)}&filter=(PARTICIPANTCODE=%27${PARTICIPANTCODE}%27)(MARKET%20in%20(%${MARKET_SH}%27,%${MARKET_SZ}%27))(HDDATE=^${DATE}^)&type=HSGTNHDDET&rt=53713501'
    },
    'sh': {
        'market_code': '27001'
    },
    'sz': {
        'market_code': '27003'
    }
}
