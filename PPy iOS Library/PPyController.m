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
+ (PPyController *)sharedPPy {
    static PPyController *shared = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        shared = [[self alloc] init];
    });
    return shared;
}
- (id)init {
    if (self = [super init]) {
        //someProperty = [[NSString alloc] initWithString:@"Default Property Value"];
    }
    return self;
}

-(void)registerDeviceWithUserDict:(NSDictionary*)userDict{
    
}
@end
