//
//  PPyController.h
//  PPydemo
//
//  Created by Pedro Piñera Buendía on 24/03/13.
//  Copyright (c) 2013 CocoaControls. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface PPyController : NSObject{
    
}
+ (PPyController *)sharedInstance;
+(void)registerDeviceWithUserDict:(NSDictionary*)userDict;

@end
