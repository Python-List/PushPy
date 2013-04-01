//
//  PPyController.m
//  PPydemo
//
//  Created by Pedro Piñera Buendía on 24/03/13.
//  Copyright (c) 2013 CocoaControls. All rights reserved.
//

#import "PPyController.h"
#import "SecureUDID.h"
@implementation PPyController{
}
@synthesize serverUrlString;
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
        
    }
    return self;
}
-(void)initializeWithAddress:(NSString*)address andPort:(NSString*)port{
    serverUrlString=[NSString stringWithFormat:@"%@:%@/pushpy/user",address,port];
}

-(void)registerDeviceWithUserDict:(NSDictionary*)userDict{
        dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{

        NSString *token=[userDict objectForKey:@"token"];
        NSString *language=[userDict objectForKey:@"language"];
        BOOL enabled=[[userDict objectForKey:@"enabled"] boolValue];
    
        //Getting the TOKEN
        NSString* devicetoken = [[[[token description]
                                   stringByReplacingOccurrencesOfString: @"<" withString: @""]
                                  stringByReplacingOccurrencesOfString: @">" withString: @""]
                                 stringByReplacingOccurrencesOfString: @" " withString: @""] ;

        //Getting the UDID
        NSString *domain = @"com.PPinera.pushpy";
        NSString *key = @"15asgsgoasui2123";
        NSString *udid = [SecureUDID UDIDForDomain:domain usingKey:key];
    
        //Getting the date
        NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
        [dateFormatter setDateFormat:@"dd-MM-yyyy"];
        NSString *last = [dateFormatter stringFromDate:[NSDate date]];
        
        
        //Generating the dict
        NSDictionary *dict=[[NSDictionary alloc] initWithObjectsAndKeys:language,@"language",udid,@"udid",[NSNumber numberWithBool:enabled],@"push",last,@"last",devicetoken,@"token", nil];
        NSError *error;
        NSData* jsonData = [NSJSONSerialization dataWithJSONObject:dict
                                                           options:NSJSONWritingPrettyPrinted error:&error];
        if(!error){
            NSString *jsonstring=[[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
            NSLog(@"> PUSHPY: User data to update: %@",jsonstring);
            
            //Sending Data
            NSString *postLength = [NSString stringWithFormat:@"%d", [jsonData length]];
            
            NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
            
            [request setURL:[NSURL URLWithString:self.serverUrlString]];
            [request setHTTPMethod:@"POST"];
            [request setValue:postLength forHTTPHeaderField:@"Content-Length"];
            [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
            [request setHTTPBody:jsonData];
            
            NSURLResponse *response;
            NSError *err;
            NSData *returnData = [ NSURLConnection sendSynchronousRequest: request returningResponse:&response error:&err];
            returnData=nil;
            NSHTTPURLResponse* httpResponse = (NSHTTPURLResponse*)response;
            int code = [httpResponse statusCode];
            NSLog(@"> PUSHPY: Update result: %d", code);
            
        }
        });
}
@end
