//
//  PPyController.m
//  PPydemo
//
//  Created by Pedro Piñera Buendía on 24/03/13.
//  Copyright (c) 2013 CocoaControls. All rights reserved.
//

#import "PPyController.h"

@implementation PPyController{
    
}
#pragma mark - init
+ (PPyController *)sharedInstance {
    if (sharedInstance!=nil) {
        return sharedInstance;
    }
    
    static dispatch_once_t pred;        // Lock
    dispatch_once(&pred, ^{             // This code is called at most once per app
        singleton = [[SingletonClass alloc] init];
    });
    
    return singleton;
}

+(void)registerDeviceWithUserDict:(NSDictionary*)userDict{
    
}
@end
